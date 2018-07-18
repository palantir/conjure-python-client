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

from .._lib import (
    ConjureBeanType,
    ConjureEnumType,
    ConjureTypeType,
    ConjureUnionType,
    DictType,
    ListType,
    OptionalType
)
from typing import Optional
from typing import Dict, Any, List
import inspect
import json


class ConjureDecoder(object):
    """Decodes json into a conjure object"""

    @classmethod
    def decode_conjure_bean_type(cls, obj, conjure_type):
        """Decodes json into a conjure bean type (a plain bean, not enum
        or union).

        Args:
            obj: the json object to decode
            conjure_type: a class object which is the bean type
                we're decoding into
        Returns:
            A instance of a bean of type conjure_type.
        """
        deserialized = {}  # type: Dict[str, Any]
        for (python_arg_name, field_definition) \
                in conjure_type._fields().items():
            field_identifier = field_definition.identifier

            if field_identifier not in obj or obj[field_identifier] is None:
                cls.check_null_field(
                    obj, deserialized, python_arg_name, field_definition)
            else:
                value = obj[field_identifier]
                field_type = field_definition.field_type
                deserialized[python_arg_name] = \
                    cls.do_decode(value, field_type)
        return conjure_type(**deserialized)

    @classmethod
    def check_null_field(
            cls, obj, deserialized, python_arg_name, field_definition):
        if isinstance(field_definition.field_type, ListType):
            deserialized[python_arg_name] = []
        elif isinstance(field_definition.field_type, DictType):
            deserialized[python_arg_name] = {}
        elif isinstance(field_definition.field_type, OptionalType):
            deserialized[python_arg_name] = None
        else:
            raise Exception(
                "field {} not found in object {}".format(
                    field_definition.identifier, obj
                )
            )

    @classmethod
    def decode_conjure_union_type(cls, obj, conjure_type):
        """Decodes json into a conjure union type.

        Args:
            obj: the json object to decode
            conjure_type: a class object which is the union type
                we're decoding into
        Returns:
            An instance of type conjure_type.
        """
        type_of_union = obj["type"]  # type: str
        for attr, conjure_field in conjure_type._options().items():
            if conjure_field.identifier == type_of_union:
                attribute = attr
                conjure_field_definition = conjure_field
                break
        else:
            raise ValueError(
                "unknown union type {0} for {1}".format(
                    type_of_union, conjure_type
                )
            )

        deserialized = {}  # type: Dict[str, Any]
        if type_of_union not in obj or obj[type_of_union] is None:
            cls.check_null_field(obj, deserialized, conjure_field_definition)
        else:
            value = obj[type_of_union]
            field_type = conjure_field_definition.field_type
            deserialized[attribute] = cls.do_decode(value, field_type)
        return conjure_type(**deserialized)

    @classmethod
    def decode_conjure_enum_type(cls, obj, conjure_type):
        """Decodes json into a conjure enum type.

        Args:
            obj: the json object to decode
            conjure_type: a class object which is the enum type
                we're decoding into.
        Returns:
            An instance of enum of type conjure_type.
        """
        if obj in conjure_type.__members__:
            return conjure_type[obj]

        else:
            return conjure_type["UNKNOWN"]

    @classmethod
    def decode_dict(
            cls,
            obj,  # type: Dict[Any, Any]
            key_type,  # ConjureTypeType
            item_type,  # ConjureTypeType
    ):  # type: (...) -> Dict[Any, Any]
        """Decodes json into a dictionary, handling conversion of the
        keys/values (the keys/values may themselves require conversion).

        Args:
            obj: the json object to decode
            key_type: a class object which is the conjure type
                of the keys in this dict
            item_type: a class object which is the conjure type
                of the values in this dict
        Returns:
            A python dictionary, where the keys are instances of type key_type
            and the values are of type value_type.
        """
        if not isinstance(obj, dict):
            raise Exception("expected a python dict")

        return dict(
            map(
                lambda x: (
                    cls.do_decode(x[0], key_type),
                    cls.do_decode(x[1], item_type),
                ),
                obj.items(),
            )
        )

    @classmethod
    def decode_list(cls, obj, element_type):
        # type: (List[Any], ConjureTypeType) -> List[Any]
        """Decodes json into a list, handling conversion of the elements.

        Args:
            obj: the json object to decode
            element_type: a class object which is the conjure type of
                the elements in this list.
        Returns:
            A python list where the elements are instances of type
                element_type.
        """
        if not isinstance(obj, list):
            raise Exception("expected a python list")

        return list(map(lambda x: cls.do_decode(x, element_type), obj))

    @classmethod
    def decode_optional(cls, obj, object_type):
        # type: (Optional[Any], ConjureTypeType) -> Optional[Any]
        """Decodes json into an element, returning None if the provided object
        is None.

        Args:
            obj: the json object to decode
            object_type: a class object which is the conjure type of
                the object if present.
        Returns:
            The decoded obj or None if no obj is provided.
        """
        if obj is None:
            return None

        return cls.do_decode(obj, object_type)

    @classmethod
    def decode_primitive(cls, obj, object_type):
        def raise_mismatch():
            raise Exception(
                'Expected to find {} type but found {} instead'.format(
                    object_type, type(obj)))

        if object_type == float:
            return float(obj)
        elif object_type == str:
            # Python 2/3 compatible way of checking string
            if not (isinstance(obj, str)
                    or str(type(obj)) == "<type 'unicode'>"):
                raise_mismatch()
        elif not isinstance(obj, object_type):
            raise_mismatch()

        return obj

    @classmethod
    def do_decode(cls, obj, obj_type):
        # type: (Any, ConjureTypeType) -> Any
        """Decodes json into the specified type

        Args:
            obj: the json object to decode
            element_type: a class object which is the type we're decoding into.
        """
        if inspect.isclass(obj_type) and issubclass(  # type: ignore
                obj_type, ConjureBeanType
        ):
            return cls.decode_conjure_bean_type(obj, obj_type)  # type: ignore

        elif inspect.isclass(obj_type) and issubclass(  # type: ignore
                obj_type, ConjureUnionType
        ):
            return cls.decode_conjure_union_type(obj, obj_type)

        elif inspect.isclass(obj_type) and issubclass(  # type: ignore
                obj_type, ConjureEnumType
        ):
            return cls.decode_conjure_enum_type(obj, obj_type)

        elif isinstance(obj_type, DictType):
            return cls.decode_dict(obj, obj_type.key_type, obj_type.value_type)

        elif isinstance(obj_type, ListType):
            return cls.decode_list(obj, obj_type.item_type)

        elif isinstance(obj_type, OptionalType):
            return cls.decode_optional(obj, obj_type.item_type)

        return cls.decode_primitive(obj, obj_type)

    def decode(self, obj, obj_type):
        # type: (Any, ConjureTypeType) -> Any
        return self.do_decode(obj, obj_type)

    def read_from_string(self, string_value, obj_type):
        # type: (str, ConjureTypeType) -> Any
        deserialized = json.loads(string_value)
        return self.decode(deserialized, obj_type)
