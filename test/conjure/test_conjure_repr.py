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
from conjure_python_client import ServiceConfiguration, RequestsClient, Service
from test.generated.conjure_verification import (
    IntegerExample, StringExample, ListExample, MapExample,
    OptionalExample, EnumExample, EnumFieldExample, EmptyObjectExample
)

@pytest.mark.parametrize('obj', [
    IntegerExample(10),
    StringExample('Hello World'),
    ListExample(['a', 'b']),
    MapExample({'a': 1, 'b': 2}),
    OptionalExample(None),
    OptionalExample('Hello World'),
    EnumFieldExample(EnumExample.ONE),
    EmptyObjectExample(),
    # Union(string_example='Hello World'), # https://github.palantir.build/foundry/conjure-python/issues/66
    # Union(this_field_is_an_integer=10)   # https://github.palantir.build/foundry/conjure-python/issues/66
])
def test_repr(obj):
    assert eval(repr(obj)) == obj


def test_repr_service():
    config = ServiceConfiguration()
    config.uris = ['http://one/', 'http://two/']
    service = RequestsClient.create(Service, "user-agent", config)
    assert repr(service) == \
        'Service(requests_session=requests.Session(...), uris=[\'http://one/\', \'http://two/\'])'
