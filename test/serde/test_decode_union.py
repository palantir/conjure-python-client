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
from conjure_python_client import ConjureDecoder, ListType, ConjureUnionType, ConjureFieldDefinition

class TestUnion(ConjureUnionType):
    _a = None
    _b = None
    _c = None

    @classmethod
    def _options(cls):
        return {
            'a': ConjureFieldDefinition('A', str),
            'b': ConjureFieldDefinition('B', int),
            'c': ConjureFieldDefinition('C', ListType(int))
            }

    def __init__(self, a=None, b=None, c=None):
        if a is not None:
            self._a = a
            self._type = 'A'
        elif b is not None:
            self._b = b
            self._type = 'B'
        elif c is not None:
            self._c = c
            self._type = 'C'

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c


def test_union_decoder():
    decoded_A = ConjureDecoder().read_from_string('{"type":"A", "A": "foo"}', TestUnion)
    decoded_B = ConjureDecoder().read_from_string('{"type":"B", "B": 5}', TestUnion)
    decoded_A2 = ConjureDecoder().read_from_string('{"type":"A", "A": "bar"}', TestUnion)
    decoded_C = ConjureDecoder().read_from_string('{"type":"C"}', TestUnion)
    assert type(decoded_A) is TestUnion
    assert type(decoded_B) is TestUnion
    assert type(decoded_C) is TestUnion
    assert decoded_A != decoded_B
    assert decoded_A != decoded_A2
    assert decoded_C != decoded_A
    assert not decoded_C.c

def test_invalid_decode():
    with pytest.raises(Exception):
        decoded_invalid = ConjureDecoder().read_from_string('{"type":"A", "B": "bar"}', TestUnion)
    

