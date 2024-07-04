from dataclasses import is_dataclass, fields
from typing import Union, List, Dict, get_args, get_origin

_NON_GENERIC_TYPES = (str, int, float, bool, type(None))


def _deserialize_non_generic(data, datatype):
    if data is None:
        return data
    return datatype(data)


def _deserialize_dict(data, datatype):
    k_arg, v_arg = get_args(datatype)
    return {
        _deserialize_data(k, k_arg): _deserialize_data(v, v_arg)
        for k, v in data.items()
    }


def _deserialize_list(data, datatype):
    arg = get_args(datatype)[0]
    return [_deserialize_data(item, arg) for item in data]


def _deserialize_union(data, datatype):
    union_types = get_args(datatype)
    for union_type in union_types:
        try:
            data = _deserialize_data(data, union_type)
            return data
        except (ValueError, TypeError, KeyError, NameError):
            pass
    raise ValueError(f"Cannot deserialize value '{data}' to types {union_types}")


def _deserialize_dataclass(data, datatype):
    data_fields = fields(datatype)
    kwargs = {}
    for field in data_fields:
        field_name = field.name
        field_type = field.type
        value = data.get(field_name)
        kwargs[field_name] = _deserialize_data(value, field_type)
    return datatype(**kwargs)


def _deserialize_data(data, datatype):
    if isinstance(data, _NON_GENERIC_TYPES):
        pass
    if is_dataclass(datatype):
        return _deserialize_dataclass(data, datatype)
    original_type = get_origin(datatype)
    if original_type == Union:
        return _deserialize_union(data, datatype)
    if original_type == list:
        return _deserialize_list(data, datatype)
    if original_type == dict:
        return _deserialize_dict(data, datatype)
    raise ValueError(
        f"Cannot deserialize value '{data}' to type '{datatype.__class__.__name__} to JSON"
    )


def deserialize(data, datatype: type):
    """Deserializes a JSON-read Python dict into a given dataclass model.
    The given JSON object is already assumed to be validated on the given model.

    Args:
        - json_obj (bytes):
    """
    if is_dataclass(datatype):
        return ValueError(f"Type '{datatype.__class__.__name__}' is not a dataclass")
    return _deserialize_data(data, datatype)
