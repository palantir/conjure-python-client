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

    _field_c = None # type: int
    _field_b = None # type: str
    _field_a = None # type: List[int]

    @classmethod
    def _options(cls):
        # type: () -> Dict[str, ConjureFieldDefinition]
        return {
            'field_c': ConjureFieldDefinition('fieldC', int),
            'field_b': ConjureFieldDefinition('fieldB', str),
            'field_a': ConjureFieldDefinition('fieldA', ListType(int))
        }

    def __init__(self, field_c=None, field_b=None, field_a=None):
        if (field_c is not None) + (field_b is not None) + (field_a is not None) != 1:
            raise ValueError('a union must contain a single member')

        if field_c is not None:
            self._field_c = field_c
            self._type = 'fieldC'
        if field_b is not None:
            self._field_b = field_b
            self._type = 'fieldB'
        if field_a is not None:
            self._field_a = field_a
            self._type = 'fieldA'

    @property
    def field_c(self):
        # type: () -> int
        return self._field_c

    @property
    def field_b(self):
        # type: () -> str
        return self._field_b

    @property
    def field_a(self):
        # type: () -> List[int]
        return self._field_a

    def accept(self, visitor):
        # type: (TestUnionVisitor) -> Any
        if not isinstance(visitor, TestUnionVisitor):
            raise ValueError('{} is not an instance of TestUnionVisitor'.format(visitor.__class__.__name__))
        if self.type == 'fieldC':
            return visitor._field_c(self.field_c)
        if self.type == 'fieldB':
            return visitor._field_b(self.field_b)
        if self.type == 'fieldA':
            return visitor._field_a(self.field_a)


def test_union_decoder():
    decoded_A = ConjureDecoder().read_from_string('{"type":"fieldB", "fieldB": "foo"}', TestUnion)
    decoded_B = ConjureDecoder().read_from_string('{"type":"fieldC", "fieldC": 5}', TestUnion)
    decoded_A2 = ConjureDecoder().read_from_string('{"type":"fieldB", "fieldB": "bar"}', TestUnion)
    decoded_A3 = ConjureDecoder().read_from_string('{"type":"fieldB", "fieldB": "bar"}', TestUnion)
    decoded_C = ConjureDecoder().read_from_string('{"type":"fieldA"}', TestUnion)
    assert type(decoded_A) is TestUnion
    assert type(decoded_B) is TestUnion
    assert type(decoded_C) is TestUnion
    assert decoded_A != decoded_B
    assert decoded_A != decoded_A2
    assert decoded_C != decoded_A
    assert decoded_A3 == decoded_A2
    assert not decoded_C.field_a

def test_invalid_decode():
    with pytest.raises(ValueError):
        decoded_invalid = ConjureDecoder().read_from_string('{"type":"fieldC", "fieldB": "bar"}', TestUnion)
    

