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

from typing import List, Dict, Type, Any, Union
from enum import Enum

from .case import to_snake_case
from .sanitize import sanitize_identifier


class ConjureType(object):
    pass


DecodableType = Union[
    int, float, bool, str, ConjureType, List[Any], Dict[Any, Any]
]


class ListType(ConjureType):
    item_type = None  # type: Type[DecodableType]

    def __init__(self, item_type):
        # type: (Type[DecodableType]) -> None
        self.item_type = item_type


class DictType(ConjureType):
    key_type = None  # type: Type[DecodableType]
    value_type = None  # type: Type[DecodableType]

    def __init__(self, key_type, value_type):
        # type: (Type[DecodableType], Type[DecodableType]) -> None
        self.key_type = key_type
        self.value_type = value_type


class OptionalType(ConjureType):
    item_type = None  # type: Type[DecodableType]

    def __init__(self, item_type):
        # type: (Type[DecodableType]) -> None
        self.item_type = item_type


class BinaryType(ConjureType):
    pass


class ConjureEnumType(ConjureType, Enum):

    # override __format__ of ConjureEnumType to prevent issue with default
    # Enum behaviour due to lack of __format__ method on ConjureType
    def __format__(self, format_spec):
        return self.__str__()

    def __repr__(self):
        return "{}.{}".format(self.__class__.__name__, self.value)


class ConjureBeanType(ConjureType):

    @classmethod
    def _fields(cls):
        # type: () -> Dict[str, ConjureFieldDefinition]
        """_fields is a mapping from constructor argument
        name to the field definition"""
        return {}

    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, self.__class__):
            return False

        for attr in self._fields():
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __ne__(self, other):
        # type: (Any) -> bool
        return not self == other

    def __repr__(self):
        # type: () -> str
        fields = [
            "{}={}".format(attr, repr(getattr(self, attr)))
            for attr, field_def in self._fields().items()
        ]
        return "{}({})".format(self.__class__.__name__, ", ".join(fields))


ConjureTypeType = Union[ConjureType, Type[DecodableType]]


class ConjureUnionType(ConjureType):
    _type = None  # type: str

    @property
    def type(self):
        # type: () -> str
        """the member name present in this union"""
        return self._type

    @classmethod
    def _options(cls):
        # type: () -> Dict[str, ConjureFieldDefinition]
        """_options defines a mapping from each member in the union
        to the field definition for that type"""
        return {}

    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, self.__class__):
            return False

        assert isinstance(other, ConjureUnionType)

        pythonic_sanitized_identifier = \
            sanitize_identifier(to_snake_case(self.type))

        return other.type == self.type and \
            getattr(self, pythonic_sanitized_identifier) == \
            getattr(other, pythonic_sanitized_identifier)

    def __ne__(self, other):
        # type: (Any) -> bool
        return not self == other

    def __repr__(self):
        # type: () -> str
        fields = [
            "{}={}".format(attr, repr(getattr(self, attr)))
            for attr, field_def in self._options().items()
            if getattr(self, attr) is not None
        ]
        return "{}({})".format(self.__class__.__name__, ", ".join(fields))


class ConjureFieldDefinition(object):
    identifier = None  # type: str
    field_type = None  # type: ConjureTypeType

    def __init__(self, identifier, field_type):
        # type: (str, ConjureTypeType) -> None
        self.identifier = identifier
        self.field_type = field_type
