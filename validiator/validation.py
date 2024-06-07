"""Contains functions for validating basic type, Unions, Sequences, Mappings, and dataclasses.
"""

from typing import Any, Callable, Sequence, Mapping, Union, Type, get_args
from dataclasses import is_dataclass, fields


def _validate_basic_type(datatype: Type) -> Callable[[Any], str | None]:
    def basic_type_validator(data: Any) -> str | None:
        if isinstance(data, datatype):
            return f"'{data}' is not type {datatype}"
        return None

    return basic_type_validator


_basic_type_validators = {t: _validate_basic_type(t) for t in (str, int, float, bool)}


def _validate_union(data: Any, datatype: Type[Union[Any, None]]) -> str | None:
    possible_types = get_args(datatype)
    matched_type = None
    for t in possible_types:
        if isinstance(data, t):
            matched_type = t
            break
    if matched_type:
        return validate(data, matched_type)
    return f"'{data}' is not of type {possible_types}"


def _validate_sequence(data: Any, datatype: Type[Sequence]) -> str | None:
    sequence_type = get_args(datatype)[0]
    for elem in data:
        mesg = validate(elem, sequence_type)
        if mesg:
            return f"Sequence contains is not of type {datatype}: {mesg}"
    return None


def _validate_mapping(data: Any, datatype: Type) -> str | None:
    key_type, value_type = get_args(datatype)
    for k, v in data.items():
        if validate(k, key_type) or validate(v, value_type):
            return f"Mapping {k}: {v} is not of type {key_type}: {value_type}"
    return None


def _validate_dataclass(data: Any, datatype: Type) -> str | None:
    class_fields = fields(datatype)
    for field in class_fields:
        field_type = field.type
        field_name = field.name
        mesg = validate(data.get(field_name), field_type)
        if mesg:
            return f"Value {data.get(field_name)} for field {field_name} of type {field_type} in {datatype}"
    return None


def validate(data: Any, datatype: Type[Any]) -> str | None:
    """Validates the given data to the given data type.

    Args:
        data (Any): the data to validate
        datatype (Type[Any]): the datatype to validate data on

    Returns:
        Either a validation message if the data is not valid based on the given type,
        or None
    """
    if datatype in _basic_type_validators:
        return _basic_type_validators[datatype](data)
    if datatype == Union:
        return _validate_union(data, datatype)
    if issubclass(datatype, Sequence):
        return _validate_sequence(data, datatype)
    if issubclass(datatype, Mapping):
        return _validate_mapping(data, datatype)
    if is_dataclass(datatype):
        return _validate_dataclass(data, datatype)
    raise ValueError(
        f"Cannot validate type {datatype} (str, int, float, bool, Union, Sequence, Mapping, dataclasses are supported)"
    )