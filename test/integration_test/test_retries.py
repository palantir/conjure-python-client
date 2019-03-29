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

import pytest
import requests
import socket
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from conjure_python_client import RequestsClient, ServiceConfiguration
from ..generated.conjure_verification_server import (
    AutoDeserializeConfirmService,
    AutoDeserializeService
)
import mock


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass
    
    def do_POST(self):
        pass


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


@pytest.fixture()
def server():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()

    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)

    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()

    yield mock_server

    mock_server.shutdown()


@pytest.fixture()
def config(server):
    config = ServiceConfiguration()
    config.uris = ["http://localhost:{port}/".format(port=server.server_port)]
    return config


@pytest.fixture()
def get_service(config):
    return RequestsClient.create(AutoDeserializeService, 'conjure-python/0.0.0', config)


@pytest.fixture()
def post_service(config):
    return RequestsClient.create(AutoDeserializeConfirmService, 'conjure-python/0.0.0', config)


def test_retry_get_on_429(server, get_service):
    calls = {'count': 0} # use mutable object to work around python 2

    def new_method(self):
        calls['count'] += 1
        self.send_response(requests.codes.too_many_requests)
        self.end_headers()
        return

    with mock.patch.object(MockServerRequestHandler, 'do_GET', new=new_method):
        with pytest.raises(requests.exceptions.RetryError):
            result = get_service.receive_integer_example(1)

    assert calls['count'] == 5


def test_retry_post_on_429(server, post_service):
    calls = {'count': 0} # use mutable object to work around python 2

    def new_method(self):
        calls['count'] += 1
        self.send_response(requests.codes.too_many_requests)
        self.end_headers()
        return

    with mock.patch.object(MockServerRequestHandler, 'do_POST', new=new_method):
        with pytest.raises(requests.exceptions.RetryError):
            result = post_service.confirm('body', 'endpoint', 'index')

    assert calls['count'] == 5