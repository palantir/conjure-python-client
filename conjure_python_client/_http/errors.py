# (c) Copyright 2025 Palantir Technologies Inc. All rights reserved.
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

from enum import Enum


class ErrorCode(str, Enum):
    """Conjure error codes as defined in the Conjure specification."""

    PERMISSION_DENIED = "PERMISSION_DENIED"
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    REQUEST_ENTITY_TOO_LARGE = "REQUEST_ENTITY_TOO_LARGE"
    FAILED_PRECONDITION = "FAILED_PRECONDITION"
    INTERNAL = "INTERNAL"
    TIMEOUT = "TIMEOUT"
    CUSTOM_CLIENT = "CUSTOM_CLIENT"
    CUSTOM_SERVER = "CUSTOM_SERVER"

    def __str__(self) -> str:
        """Return just the string value"""
        return self.value
