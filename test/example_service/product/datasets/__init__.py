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
from conjure import *
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

class BackingFileSystem(ConjureBeanType):

    @classmethod
    def _fields(cls):
        # type: () -> Dict[str, ConjureFieldDefinition]
        return {
            'file_system_id': ConjureFieldDefinition('fileSystemId', str),
            'base_uri': ConjureFieldDefinition('baseUri', str),
            'configuration': ConjureFieldDefinition('configuration', DictType(str, str))
        }

    _file_system_id = None # type: str
    _base_uri = None # type: str
    _configuration = None # type: Dict[str, str]

    def __init__(self, file_system_id, base_uri, configuration):
        # type: (str, str, Dict[str, str]) -> None
        self._file_system_id = file_system_id
        self._base_uri = base_uri
        self._configuration = configuration

    @property
    def file_system_id(self):
        # type: () -> str
        '''The name by which this file system is identified.'''
        return self._file_system_id

    @property
    def base_uri(self):
        # type: () -> str
        return self._base_uri

    @property
    def configuration(self):
        # type: () -> Dict[str, str]
        return self._configuration

class Dataset(ConjureBeanType):

    @classmethod
    def _fields(cls):
        # type: () -> Dict[str, ConjureFieldDefinition]
        return {
            'file_system_id': ConjureFieldDefinition('fileSystemId', str),
            'rid': ConjureFieldDefinition('rid', str)
        }

    _file_system_id = None # type: str
    _rid = None # type: str

    def __init__(self, file_system_id, rid):
        # type: (str, str) -> None
        self._file_system_id = file_system_id
        self._rid = rid

    @property
    def file_system_id(self):
        # type: () -> str
        return self._file_system_id

    @property
    def rid(self):
        # type: () -> str
        '''Uniquely identifies this dataset.'''
        return self._rid

