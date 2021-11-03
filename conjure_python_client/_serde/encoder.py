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

from .._lib import ConjureBeanType, ConjureUnionType, ConjureEnumType
from math import isnan, isinf
from typing import Dict, Any, Union, List
import json
import base64


class ConjureEncoder(json.JSONEncoder):
    """Transforms a conjure type into json"""

    @classmethod
    def encode_conjure_bean_type(cls, obj):
        # type: (ConjureBeanType) -> Any
        """Encodes a conjure bean into json"""
        encoded = {}  # type: Dict[str, Any]
        for attribute_name, field_definition in obj._fields().items():
            encoded[field_definition.identifier] = cls.do_encode(
                getattr(obj, attribute_name)
            )
        return encoded

    @classmethod
    def encode_conjure_union_type(cls, obj):
        # type: (ConjureUnionType) -> Any
        """Encodes a conjure union into json"""
        encoded = {}  # type: Dict[str, Any]
        encoded["type"] = obj.type
        for attr, field_definition in obj._options().items():
            if field_definition.identifier == obj.type:
                attribute = attr
                break
        else:
            raise ValueError(
                "could not find attribute for union " +
                "member {0} of type {1}".format(obj.type, obj.__class__)
            )

        defined_field_definition = obj._options()[attribute]
        encoded[defined_field_definition.identifier] = cls.do_encode(
            getattr(obj, attribute)
        )
        return encoded

    @classmethod
    def encode_primitive(cls, obj):
        if isinstance(obj, float) and isnan(obj):
            return 'NaN'
        if isinstance(obj, float) and isinf(obj):
            return '{}Infinity'.format('-' if obj < 0 else '')
        return obj

    @classmethod
    def do_encode(cls, obj):
        # type: (Any) -> Any
        """Encodes the passed object into json"""
        if isinstance(obj, ConjureBeanType):
            return cls.encode_conjure_bean_type(obj)

        elif isinstance(obj, ConjureUnionType):
            return cls.encode_conjure_union_type(obj)

        elif isinstance(obj, ConjureEnumType):
            return obj.value

        elif isinstance(obj, list):
            return list(map(cls.do_encode, obj))

        elif isinstance(obj, dict):
            return {cls.do_encode(key): cls.do_encode(value)
                    for key, value in obj.items()}

        else:
            return cls.encode_primitive(obj)

    def default(self, obj):
        # type: (Any) -> Any
        return self.do_encode(obj)

    def plain(self, obj):
        # type: (Any) -> Union[List[str], str]
        """PLAIN-encode object for use in header / path / query params"""
        if isinstance(obj, ConjureBeanType) \
                or isinstance(obj, ConjureUnionType) \
                or isinstance(obj, dict):
            raise ValueError("Cannot PLAIN-encode complex types")

        # lists and sets are ok in query params (&param=...&param=...)
        if isinstance(obj, list) or isinstance(obj, set):
            return [self.plain_primitive(inner) for inner in obj]

        return self.plain_primitive(obj)

    def plain_primitive(self, obj):
        # type: (Any) -> str
        # strings in their unquoted form (client does URL-encoding)
        # this covers bearertoken / rid / uuid / datetime / string
        if isinstance(obj, str):
            return obj

        # binary as base64 encoded string
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode('ascii')

        # floats as the number value or special NaN / Infinity values
        if isinstance(obj, float):
            if isnan(obj):
                return 'NaN'
            if isinf(obj):
                return '{}Infinity'.format('-' if obj < 0 else '')
            return str(obj)

        # bool as lowercase bool
        # NB: bools are ints so this test has to be first
        if isinstance(obj, bool):
            return str(obj).lower()

        # ints (and safelong) as just the number
        if isinstance(obj, int):
            return str(obj)

        # unquoted variant name
        if isinstance(obj, ConjureEnumType):
            return obj.value

        raise ValueError("Cannot PLAIN-encode type: " + type(obj))
