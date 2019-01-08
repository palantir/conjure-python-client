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
from conjure_python_client import ConjureDecoder, ConjureEncoder, SetType


def test_set_with_well_typed_items_decodes():
    decoded = ConjureDecoder().read_from_string("[1,2,3]", SetType(int))
    assert type(decoded) is frozenset
    assert type(list(decoded)[0]) is int


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
