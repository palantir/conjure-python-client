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
from conjure_python_client import ConjureEncoder


def test_float_encodes():
    encoded = ConjureEncoder.encode_primitive(1.0)
    assert(type(encoded) is float)


def test_nan_float_encodes():
    encoded = ConjureEncoder.encode_primitive(float('nan'))
    assert(encoded == 'NaN')


@pytest.mark.parametrize("value,expected_encoded", [
    (float('inf'), 'Infinity'),
    (-float('inf'), '-Infinity'),
])
def test_inf_float_encodes(value, expected_encoded):
    encoded = ConjureEncoder.encode_primitive(value)
    assert(encoded == expected_encoded)

