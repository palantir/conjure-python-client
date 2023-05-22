# (c) Copyright 2023 Palantir Technologies Inc. All rights reserved.
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
from conjure_python_client import ConjureDecoder
from test.generated.conjure_verification_types import Union


def test_union_with_unknown_type_fails():
    with pytest.raises(ValueError) as e:
        ConjureDecoder().read_from_string(
            '{"type": "unknown", "unknown": "unknown_value"}', Union, False
        )
    assert e.match(
        "unknown union type unknown for <class 'generated.conjure_verification_types.Union'>"
    )


def test_union_with_unknown_type_and_return_none_for_unknown_types_succeeds():
    decoded = ConjureDecoder().read_from_string(
        '{"type": "unknown", "unknown": "unknown_value"}', Union, True
    )
    assert decoded is None
