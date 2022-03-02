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
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SslConfiguration:
    trust_store_path: str


@dataclass
class ServiceConfiguration:
    api_token: Optional[str] = None
    security: Optional[SslConfiguration] = None
    uris: List[str] = field(default_factory=list)
    connect_timeout: float = 10
    read_timeout: float = 300
    max_num_retries: int = 4
    backoff_slot_size: int = 250
