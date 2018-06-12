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
import re
from conjure import ConjureDecoder
from test.example_service.product import CreateDatasetRequest


def test_object_decodes_when_exact_fields_are_present():
    decoded = ConjureDecoder().read_from_string(
        """{"fileSystemId": "foo", "path": "bar"}""", CreateDatasetRequest
    )
    assert decoded == CreateDatasetRequest("foo", "bar")


def test_object_with_extra_fields_should_only_keep_expected_fields():
    decoded = ConjureDecoder().read_from_string(
        """{"fileSystemId": "foo", "path": "bar", "redundant": 1}""",
        CreateDatasetRequest,
    )
    assert decoded == CreateDatasetRequest("foo", "bar")


def test_object_with_missing_field_should_throw_helpful_exception():
    with pytest.raises(Exception) as excinfo:
        ConjureDecoder().read_from_string(
            """{"path": "bar", "redundant": 1}""", CreateDatasetRequest
        )
    message_regex = re.compile("field fileSystemId not found in object {.+}")
    assert message_regex.match(str(excinfo.value)), excinfo.value


def test_object_with_wrong_type_field_should_throw_helpful_exception():
    decoded = ConjureDecoder().read_from_string(
        """{"fileSystemId": "foo", "path": 999}""", CreateDatasetRequest
    )
    # captures current (broken) behaviour
    assert decoded == CreateDatasetRequest("foo", 999)


@pytest.mark.skip(reason="not implemented")
def test_object_with_wrong_type_field_should_throw_helpful_exception_TODO():
    with pytest.raises(Exception) as excinfo:
        ConjureDecoder().read_from_string(
            """{"fileSystemId": "foo", "path": 999}""", CreateDatasetRequest
        )
    assert " some useful exception saying path: 999 should be a string" in str(
        excinfo.value
    )


def test_object_with_null_field_should_throw_helpful_exception():
    decoded = ConjureDecoder().read_from_string(
        """{"fileSystemId": null, "path": "bar"}""", CreateDatasetRequest
    )
    # captures current (broken) behaviour
    assert decoded == CreateDatasetRequest(None, "bar")


@pytest.mark.skip(reason="not implemented")
def test_object_with_null_field_should_throw_helpful_exception_TODO():
    with pytest.raises(Exception) as excinfo:
        ConjureDecoder().read_from_string(
            """{"fileSystemId": null, "path": "bar"}""", CreateDatasetRequest
        )
    assert " some useful exception saying fileSystem: null should be a string" in str(
        excinfo.value
    )
