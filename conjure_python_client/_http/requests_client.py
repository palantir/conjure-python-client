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

import binascii
import os
import random
import requests


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


TRACE_ID_HEADER = 'X-B3-TraceId'  # type: str
TRACE_ID_RANDOM_BYTES = 8


def fresh_trace_id():
    # type: () -> bytes
    # returns a bytestring which is a valid zipkin trace id
    return binascii.hexlify(os.urandom(TRACE_ID_RANDOM_BYTES))


class Service(object):
    _requests_session = None  # type: requests.Session
    _uris = None  # type: List[str]
    _connect_timeout = None  # type: float
    _read_timeout = None  # type: float
    _verify = None  # type: str

    def __init__(
        self, requests_session, uris, _connect_timeout, _read_timeout, _verify
    ):
        # type: (requests.Session, List[str], float, float, str) -> None
        self._requests_session = requests_session
        self._uris = uris
        self._connect_timeout = _connect_timeout
        self._read_timeout = _read_timeout
        self._verify = _verify

    @property
    def _uri(self):
        # type: () -> str
        """returns a random uri"""
        return random.SystemRandom().choice(self._uris)

    def _request(self, *args, **kwargs):
        # type (Any) -> Response
        """Make requests using configured :class:`requests.Session`.
        Any error details will be extracted to an :class:`HTTPError`
        which will contain relevant error details when printed."""
        self._amend_request_kwargs(kwargs)
        _response = self._requests_session.request(*args, **kwargs)
        try:
            _response.raise_for_status()
        except HTTPError as e:
            if e.response is not None:
                raise_from(ConjureHTTPError(e), e)
            raise e
        return _response

    def __repr__(self):
        return '{}(requests_session={}, uris={})'.format(
            self.__class__.__name__,
            "requests.Session(...)",
            repr(self._uris)
        )

    def _amend_request_kwargs(self, kwargs):
        for param_kind in ['headers', 'params']:
            if param_kind in kwargs:
                kwargs[param_kind] = _clean_params(kwargs[param_kind])
        kwargs['timeout'] = (self._connect_timeout, self._read_timeout)
        kwargs['verify'] = self._verify
        _add_trace_id(kwargs)


def _clean_params(params):
    cleaned_params = {}
    for key, value in params.items():
        if value is None:
            continue
        cleaned_params[key] = _clean_param_value(value)
    return cleaned_params


def _clean_param_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _add_trace_id(kwargs):
    # type: (Dict) -> None
    # Adds the trace ID to the arguments
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers'][TRACE_ID_HEADER] = fresh_trace_id()


class RetryWithJitter(Retry):
    '''
    Extends the standard urllib Retry in order to match conjure behaviour.
    Retry times contain a uniform jitter. Additionally all http methods are
    considered valid to retry.
    '''

    def _is_method_retryable(self, method):
        return True

    def get_backoff_time(self):
        jitter = random.random()
        return jitter * super(RetryWithJitter, self).get_backoff_time()


class RequestsClient(object):

    @classmethod
    def create(cls, service_class, user_agent, service_config):
        # type: (Type[T], str, ServiceConfiguration) -> T
        # setup retry to match java remoting
        # https://github.com/palantir/http-remoting/tree/3.12.0#quality-of-service-retry-failover-throttling
        retry = RetryWithJitter(
            total=service_config.max_num_retries,
            read=0,  # do not retry read errors
            status_forcelist=[308, 429, 503],
            backoff_factor=float(service_config.backoff_slot_size) / 1000,
        )
        transport_adapter = TransportAdapter(max_retries=retry)
        # create a session, for shared connection polling, user agent, etc
        session = requests.Session()
        session.headers = {"User-Agent": user_agent}
        if service_config.security is not None:
            verify = service_config.security.trust_store_path
        else:
            verify = None
        for uri in service_config.uris:
            session.mount(uri, transport_adapter)
        return service_class(  # type: ignore
            session,
            service_config.uris,
            service_config.connect_timeout,
            service_config.read_timeout,
            verify,
        )


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
        self._trace_id = http_error.response.headers.get('X-B3-TraceId')
        try:
            detail = http_error.response.json()
            self._error_code = detail.get("errorCode")
            self._error_name = detail.get("errorName")
            self._error_instance_id = detail.get("errorInstanceId")
            self._parameters = detail.get("parameters", dict())
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
            message = "{}. TraceId: '{}'. Response: '{}'"\
                .format(
                    http_error,
                    self._trace_id,
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
