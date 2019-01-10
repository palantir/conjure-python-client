
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
from conjure_python_client import ConjureDecoder, ConjureEnumType


class TestEnum(ConjureEnumType):

    A = 'A'
    '''A'''
    B = 'B'
    '''B'''
    C = 'C'
    '''C'''
    UNKNOWN = 'UNKNOWN'
    '''UNKNOWN'''

    def __reduce_ex__(self, proto):
        return self.__class__, (self.name,)


def test_enum_decode():
    decoded_A = ConjureDecoder().read_from_string("\"A\"", TestEnum)
    decoded_B = ConjureDecoder().read_from_string("\"B\"", TestEnum)
    decoded_A2 = ConjureDecoder().read_from_string("\"A\"", TestEnum)
    assert decoded_A != decoded_B
    assert decoded_A == decoded_A2

    decoded_unk = ConjureDecoder().read_from_string("\"G\"", TestEnum)
    assert repr(decoded_unk) == "TestEnum.UNKNOWN"

    decoded_integer = ConjureDecoder().read_from_string("5", TestEnum)
    assert repr(decoded_integer) == "TestEnum.UNKNOWN"
