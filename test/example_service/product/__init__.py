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

# this is package product
from conjure_python_client import *
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple


class CreateDatasetRequest(ConjureBeanType):
    @classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            "file_system_id": ConjureFieldDefinition("fileSystemId", str),
            "path": ConjureFieldDefinition("path", str),
        }

    _file_system_id: str = None
    _path: str = None

    def __init__(self, file_system_id: str, path: str) -> None:
        self._file_system_id = file_system_id
        self._path = path

    @property
    def file_system_id(self) -> str:
        return self._file_system_id

    @property
    def path(self) -> str:
        return self._path


class SimpleService(Service):
    def testEndpoint(self, string: str, decoration: List[str] = []) -> str:

        _headers: Dict[str, Any] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        _params: Dict[str, Any] = {"decoration": decoration}

        _path_params: Dict[str, Any] = {}

        _json: Any = ConjureEncoder().default(string)

        _path = "/catalog/testEndpoint"
        _path = _path.format(**_path_params)

        _response = self._request(
            "POST",
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json,
        )

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), str)
