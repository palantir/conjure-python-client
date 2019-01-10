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
from conjure_python_client import ConjureDecoder, ConjureEncoder, SetType, ConjureUnionType, ConjureFieldDefinition

class TestUnion(ConjureUnionType):

    _field_c = None 
    _field_b = None 
    _field_a = None 

    @classmethod
    def _options(cls):
        # type: () -> Dict[str, ConjureFieldDefinition]
        return {
            'field_c': ConjureFieldDefinition('fieldC', int),
            'field_b': ConjureFieldDefinition('fieldB', str),
            'field_a': ConjureFieldDefinition('fieldA', SetType(int))
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
        return self._field_c

    @property
    def field_b(self):
        return self._field_b

    @property
    def field_a(self):
        return self._field_a


def test_set_with_well_typed_items_decodes():
    decoded = ConjureDecoder().read_from_string("[1,2,3]", SetType(int))
    assert type(decoded) is frozenset
    assert type(list(decoded)[0]) is int

def test_set_in_enum_decode():
    decoded = ConjureDecoder().read_from_string('{"type": "fieldA"}', TestUnion)
    assert type(decoded.field_a) is frozenset
    assert len(decoded.field_a) == 0

def test_set_with_one_badly_typed_item_fails():
    with pytest.raises(Exception):
        ConjureDecoder().read_from_string("""[1,"two",3]""", SetType(int))


def test_set_with_no_items_decodes():
    decoded = ConjureDecoder().read_from_string("[]", SetType(int))
    assert type(decoded) is frozenset


def test_set_from_json_object_fails():
    with pytest.raises(Exception):
        ConjureDecoder().read_from_string("{}", SetType(int))


def test_set_does_not_decode_from_json_null():
    with pytest.raises(Exception):
        ConjureDecoder().read_from_string("null", SetType(int))


def test_set_does_not_decode_from_json_string():
    with pytest.raises(Exception):
        ConjureDecoder().read_from_string("\"hello\"", SetType(int))

def test_set_encoder():
    encoded = ConjureEncoder.do_encode(frozenset([5,6,7]))
    assert type(encoded) is list
    encoded = ConjureEncoder.do_encode(set([5,6,7]))
    assert type(encoded) is list
