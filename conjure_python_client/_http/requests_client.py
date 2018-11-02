# (c) Copyright 2018 Palantir Technologies Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from requests.adapters import HTTPAdapter
from typing import TypeVar, Type, List, Optional, Dict
from requests.exceptions import HTTPError
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from requests.packages.urllib3.util import Retry
from .configuration import ServiceConfiguration
from future.utils import raise_from
import requests
import random


T = TypeVar("T")
# https://testssl.sh/openssl-rfc.mappping.html
CIPHERS = (
    "ECDHE-RSA-AES256-SHA384:"
    "ECDHE-RSA-AES128-SHA256:"
    "ECDH-RSA-AES256-SHA384:"
    "ECDH-RSA-AES128-SHA256:"
    "AES128-SHA256:"
    "AES256-SHA256:"
    "ECDHE-RSA-AES256-SHA:"
    "ECDHE-RSA-AES128-SHA:"
    "ECDH-RSA-AES256-SHA:"
    "ECDH-RSA-AES128-SHA256:"
    "AES256-SHA:"
    "AES128-SHA:"
    "TLS_FALLBACK_SCSV"
)


class Service(object):
    _requests_session = None  # type: requests.Session
    _uris = None  # type: List[str]

    def __init__(self, requests_session, uris):
        # type: (requests.Session, List[str]) -> None
        self._requests_session = requests_session
        self._uris = uris

    @property
    def _uri(self):
        # type: () -> str
        """returns a random uri"""
        return random.choice(self._uris)

    def _request(self, *args, **kwargs):
        # type (Any) -> Response
        """Make requests using configured :class:`requests.Session`.
        Any error details will be extracted to an :class:`HTTPError`
        which will contain relevant error details when printed."""
        for param_kind in ['headers', 'params']:
            if param_kind in kwargs:
                cleaned_params = {}
                for key, value in kwargs[param_kind].items():
                    if value is None:
                        continue
                    cleaned_params[key] = str(value).lower() \
                        if isinstance(value, bool) else str(value)
                kwargs[param_kind] = cleaned_params

        _response = self._requests_session.request(*args, **kwargs)
        try:
            _response.raise_for_status()
        except HTTPError as e:
            if e.response is not None and e.response.content is not None:
                raise_from(ConjureHTTPError(e), e)
            raise e
        return _response

    def __repr__(self):
        return '{}(requests_session={}, uris={})'.format(
            self.__class__.__name__,
            "requests.Session(...)",
            repr(self._uris)
        )


class RequestsClient(object):

    @classmethod
    def create(cls, service_class, user_agent, service_config):
        # type: (Type[T], str, ServiceConfiguration) -> T
        # setup retry to match java remoting
        # https://github.com/palantir/http-remoting/tree/3.12.0#quality-of-service-retry-failover-throttling
        retry = Retry(
            total=service_config.max_num_retries,
            status_forcelist=[308, 429, 503],
            backoff_factor=float(service_config.backoff_slot_size) / 1000,
        )
        transport_adapter = TransportAdapter(max_retries=retry)
        # create a session, for shared connection polling, user agent, etc
        session = requests.Session()
        session.headers = {"User-Agent": user_agent}
        if service_config.security is not None:
            session.verify = service_config.security.trust_store_path
        for uri in service_config.uris:
            session.mount(uri, transport_adapter)
        return service_class(session, service_config.uris)  # type: ignore


class TransportAdapter(HTTPAdapter):
    """Transport adapter that allows customising ssl things"""

    def init_poolmanager(
            self, connections, maxsize, block=False, **pool_kwargs
    ):
        self._pool_connections = connections
        self._pool_maxsize = maxsize
        self._pool_block = block
        ssl_context = create_urllib3_context(ciphers=CIPHERS)
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            strict=True,
            ssl_context=ssl_context,
            **pool_kwargs
        )


class ConjureHTTPError(HTTPError):
    """A an HTTPError from a Conjure Service with ``SerializableError``
    attributes extracted from the response."""

    _cause = None               # type: Optional[HTTPError]
    _error_code = None          # type: str
    _error_name = None          # type: str
    _error_instance_id = None   # type: str
    _parameters = None          # type: Dict[str, str]
    _trace_id = None            # type: str

    def __init__(self, http_error):
        # type (HTTPError) -> None
        self._cause = http_error
        try:
            detail = http_error.response.json()
            self._error_code = detail.get("errorCode")
            self._error_name = detail.get("errorName")
            self._error_instance_id = detail.get("errorInstanceId")
            self._parameters = detail.get("parameters", dict())
            self._trace_id = http_error.response.headers.get('X-B3-TraceId')
            message = "{}. ErrorCode: '{}'. ErrorName: '{}'. " \
                "ErrorInstanceId: '{}'. TraceId: '{}'. Parameters: {}" \
                .format(
                    http_error,
                    self._error_code,
                    self._error_name,
                    self._error_instance_id,
                    self._trace_id,
                    self._parameters
                )
        except ValueError:
            message = "{}. Response: '{}'"\
                .format(
                    http_error,
                    http_error.response.text
                )
        super(ConjureHTTPError, self).__init__(
            message,
            request=http_error.request,
            response=http_error.response
        )

    @property
    def cause(self):
        # type: () -> Optional[HTTPError]
        """The wrapped ``HTTPError`` that was the direct cause of
        the ``ConjureHTTPError``.
        """
        return self._cause

    @property
    def error_code(self):
        # type: () -> str
        """A fixed code word identifying the type of error."""
        return self._error_code

    @property
    def error_name(self):
        # type: () -> str
        """A fixed name identifying the error."""
        return self._error_name

    @property
    def error_instance_id(self):
        # type: () -> str
        """A unique identifier for this error instance."""
        return self._error_instance_id

    @property
    def parameters(self):
        # type: () -> Dict[str, str]
        """A set of parameters that further explain the error."""
        return self._parameters

    @property
    def trace_id(self):
        # type: () -> str
        """The X-B3-TraceId for the request."""
        return self._trace_id
