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

from conjure_python_client import (
    ConjureHTTPError,
    RequestsClient,
    ServiceConfiguration,
)
from unittest import mock
import pytest
import requests
from requests.exceptions import HTTPError
from test.example_service.product import SimpleService


class TestHttpRemoting(object):
    @staticmethod
    def _test_service() -> SimpleService:
        config = ServiceConfiguration()
        config.uris = ["https://dummy/simple/api"]
        service = RequestsClient.create(
            SimpleService, user_agent="pytest", service_config=config
        )
        return service

    @staticmethod
    def _mock_response(
        status=200,
        content="CONTENT",
        json_data=None,
        raise_for_status=None,
    ):
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(return_value=json_data)
        return mock_resp

    @mock.patch("requests.Session.request")
    def test_http_success(self, mock_request):
        mock_request.return_value = self._mock_response(json_data="bar")
        self._test_service().testEndpoint("foo")

    @mock.patch("requests.Session.request")
    def test_array_query_parameter(self, mock_request):
        mock_request.return_value = self._mock_response(json_data="bar")
        self._test_service().testEndpoint(
            "foo", decoration=["branches", "path"]
        )
        name, args, kwargs = mock_request.mock_calls[0]
        assert kwargs["params"]["decoration"] == ["branches", "path"]

    @mock.patch("requests.Session.request")
    def test_http_error(self, mock_request):
        resp = requests.Response()
        resp.status_code = 404
        resp._content = (
            b'{"errorCode":"NOT_FOUND",'
            + b'"errorName":"Default:NotFound",'
            + b'"errorInstanceId":"00000000-0000-0000-0000-000000000000",'
            + b'"parameters":{}}'
        )
        http_error = HTTPError("something", response=resp)
        mock_request.return_value = self._mock_response(
            status=404, raise_for_status=http_error
        )

        with pytest.raises(ConjureHTTPError) as e:
            self._test_service().testEndpoint("foo")
        assert e.match("Default:NotFound")
        assert e.match("00000000-0000-0000-0000-000000000000")

    @mock.patch("requests.Session.request")
    def test_http_error_not_json(self, mock_request):
        resp = requests.Response()
        resp.status_code = 404
        resp._content = b"Content that's not JSON"
        http_error = HTTPError("something", response=resp)
        mock_request.return_value = self._mock_response(
            status=404, raise_for_status=http_error
        )

        with pytest.raises(ConjureHTTPError) as e:
            self._test_service().testEndpoint("foo")
        assert e.match("Content that's not JSON")

    @mock.patch("requests.Session.request")
    def test_http_error_empty_response(self, mock_request):
        resp = requests.Response()
        resp.status_code = 500
        resp._content = b""
        http_error = HTTPError("mocked http error", response=resp)
        mock_request.return_value = self._mock_response(
            status=404, raise_for_status=http_error
        )

        with pytest.raises(ConjureHTTPError) as e:
            self._test_service().testEndpoint("foo")
        assert e.match("mocked http error. TraceId: 'None'. Response: ''")

    @mock.patch("requests.Session.request")
    def test_http_error_none_response(self, mock_request):
        resp = requests.Response()
        resp.status_code = 500
        resp._content = None
        http_error = HTTPError("mocked http error", response=resp)
        mock_request.return_value = self._mock_response(
            status=404, raise_for_status=http_error
        )

        with pytest.raises(ConjureHTTPError) as e:
            self._test_service().testEndpoint("foo")
        assert e.match("mocked http error. TraceId: 'None'. Response: ''")

    @mock.patch("requests.Session.request")
    def test_http_error_trace_id(self, mock_request):
        resp = requests.Response()
        resp.status_code = 500
        resp._content = None
        resp.headers["X-B3-TraceId"] = "faketraceid"
        http_error = HTTPError("mocked http error", response=resp)
        mock_request.return_value = self._mock_response(
            status=404, raise_for_status=http_error
        )

        with pytest.raises(ConjureHTTPError) as e:
            self._test_service().testEndpoint("foo")
        assert e.match(
            "mocked http error. TraceId: 'faketraceid'. Response: ''"
        )

    @mock.patch("requests.Session.request")
    def test_request_trace_id(self, mock_request):
        mock_request.return_value = self._mock_response(json_data="bar")
        self._test_service().testEndpoint("foo")

        call = mock_request.mock_calls[0]
        call_kwargs = call[2]
        assert "X-B3-TraceId" in call_kwargs["headers"]
        first_trace = call_kwargs["headers"]["X-B3-TraceId"]

        mock_request.reset_mock()
        self._test_service().testEndpoint("foo")

        second_call = mock_request.mock_calls[0]
        second_trace = second_call[2]["headers"]["X-B3-TraceId"]

        assert first_trace != second_trace
