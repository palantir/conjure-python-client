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
from typing import Dict, Any
import json


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
        # TODO(forozco): support inifinities
        if isinstance(obj, float) and (isnan(obj) or isinf(obj)):
            return 'NaN'
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
