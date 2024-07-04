"""Contains functions for validating basic type, Unions,
lists, dicts, and dataclasses.
"""

from types import NoneType
from typing import Any, Callable, List, Dict, Union, Type, get_args, get_origin
from dataclasses import is_dataclass, fields


def _validate_basic_type(datatype: Type) -> Callable[[Any], str | None]:
    def basic_type_validator(data: Any) -> str | None:
        if not isinstance(data, datatype):
            return f"Validate basic type: '{data}' is not type {datatype}"
        return None
    return basic_type_validator


_basic_type_validators = {
    t: _validate_basic_type(t) for t in (str, int, float, bool, NoneType)
}


def _validate_union(data: Any, datatype: Type[Union[Any, None]]) -> str | None:
    possible_types = get_args(datatype)
    mesg = None
    for t in possible_types:
        mesg = validate(data, t)
        if not mesg:
            break
    if mesg:
        return f"Validate union: could not validate data on union of types {possible_types}:\n{mesg}"
    return None


def _validate_list(data: Any, datatype: type[list]) -> str | None:
    if not isinstance(data, List):
        return "Validate list: data is not a List type"
    sequence_type = get_args(datatype)[0]
    for elem in data:
        mesg = validate(elem, sequence_type)
        if mesg:
            return f"Validate list: list contains an element not of type {datatype}:\n{mesg}"
    return None


def _validate_dict(data: Any, datatype: Type) -> str | None:
    if not isinstance(data, Dict):
        return "Validate dict: Data is not a Dict type"
    key_type, value_type = get_args(datatype)
    for k, v in data.items():
        key_mesg = validate(k, key_type)
        if key_mesg:
            return f"Validate dict: {k} not of type {key_type}:\n{key_mesg}"
        value_mesg = validate(v, value_type)
        if value_mesg:
            return f"Validate dict: {v} not of type {value_type}:\n{value_mesg}"
    return None


def _validate_dataclass(data: Dict[str, Any], datatype: Type) -> str | None:
    is_not_string_dict = validate(data, Dict[str, Any])
    if is_not_string_dict:
        return f"Validate dataclass: Data is not a string-keyed dict: {is_not_string_dict}"
    data_fields = set(data.keys())
    class_fields = fields(datatype)
    for field in class_fields:
        field_type = field.type
        field_name = field.name

        mesg = validate(data.get(field_name), field_type)
        if mesg:
            return (
                f"Validate dataclass: Value '{data.get(field_name)}' is not valid:\n{mesg}"
            )
        if field_name in data_fields:
            data_fields.remove(field_name)
    if data_fields:
        return f"Validate dataclass: Data had extra fields '{data_fields}'"
    return None


def validate(data: Any, datatype: Type[Any]) -> str | None:
    """Validates the given data loaded from JSON to the given data type.

    Args:
        data (Any): the data to validate
        datatype (Type[Any]): the datatype to validate data on

    Returns:
        Either a validation message if the data is not
        valid based on the given type,
        or None
    """
    if datatype == Any:
        return None
    if datatype in _basic_type_validators:
        return _basic_type_validators[datatype](data)
    if is_dataclass(datatype):
        return _validate_dataclass(data, datatype)
    original_type = get_origin(datatype)
    if original_type == Union:
        return _validate_union(data, datatype)
    if original_type == list:
        return _validate_list(data, datatype)
    if original_type == dict:
        return _validate_dict(data, datatype)
    raise ValueError(
        f"Cannot validate type {datatype} (must use str, int, float, "
        "bool, List, Dict, Union, or dataclasses using these types)"
    )
