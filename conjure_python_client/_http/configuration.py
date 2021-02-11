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

from typing import List, Any, Optional


class SslConfiguration(object):
    trust_store_path = None  # type: str

    def __init__(self, trust_store_path):
        # type: (str) -> None
        self.trust_store_path = trust_store_path


class ServiceConfiguration(object):
    """
    For details regarding the proxies field,
    please see https://requests.readthedocs.io/en/master/user/advanced/#proxies
    If proxies is None, system defaults will be used, as described in the Requests docs
    """
    api_token = None  # type: str
    security = SslConfiguration  # type: Any
    connect_timeout = 10  # type: float
    read_timeout = 300  # type: float
    uris = []  # type: List[str]
    max_num_retries = 4  # type: int
    backoff_slot_size = 250  # type: int
    proxies = None # type: Optional[dict[str, str]]