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

# this is package product.datasets
from conjure_python_client import *
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple


class BackingFileSystem(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            "file_system_id": ConjureFieldDefinition("fileSystemId", str),
            "base_uri": ConjureFieldDefinition("baseUri", str),
            "configuration": ConjureFieldDefinition(
                "configuration", DictType(str, str)
            ),
        }

    _file_system_id: str = None
    _base_uri: str = None
    _configuration: Dict[str, str] = None

    def __init__(
        self, file_system_id: str, base_uri: str, configuration: Dict[str, str]
    ) -> None:
        self._file_system_id = file_system_id
        self._base_uri = base_uri
        self._configuration = configuration

    @property
    def file_system_id(self) -> str:
        """The name by which this file system is identified."""
        return self._file_system_id

    @property
    def base_uri(self) -> str:
        return self._base_uri

    @property
    def configuration(self) -> Dict[str, str]:
        return self._configuration


class Dataset(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            "file_system_id": ConjureFieldDefinition("fileSystemId", str),
            "rid": ConjureFieldDefinition("rid", str),
        }

    _file_system_id: str = None
    _rid: str = None

    def __init__(self, file_system_id: str, rid: str) -> None:
        self._file_system_id = file_system_id
        self._rid = rid

    @property
    def file_system_id(self) -> str:
        return self._file_system_id

    @property
    def rid(self) -> str:
        """Uniquely identifies this dataset."""
        return self._rid


class ListExample(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {"value": ConjureFieldDefinition("value", ListType(str))}

    _value: List[str] = None

    def __init__(self, value: List[str]) -> None:
        self._value = value

    @property
    def value(self) -> List[str]:
        return self._value


class MapExample(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {"value": ConjureFieldDefinition("value", DictType(str, str))}

    _value: Dict[str, str] = None

    def __init__(self, value: Dict[str, str]) -> None:
        self._value = value

    @property
    def value(self) -> Dict[str, str]:
        return self._value


class EnumExample(ConjureEnumType):

    ONE = 'ONE'
    '''ONE'''
    TWO = 'TWO'
    '''TWO'''
    ONE_HUNDRED = 'ONE_HUNDRED'
    '''ONE_HUNDRED'''
    UNKNOWN = 'UNKNOWN'
    '''UNKNOWN'''

    def __reduce_ex__(self, proto):
        return self.__class__, (self.name,)


class EnumFieldExample(ConjureBeanType):

    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'enum': ConjureFieldDefinition('enum', EnumExample)
        }

    __slots__: List[str] = ['_enum']

    def __init__(self, enum: "EnumExample") -> None:
        self._enum = enum

    @property
    def enum(self) -> "EnumExample":
        return self._enum
