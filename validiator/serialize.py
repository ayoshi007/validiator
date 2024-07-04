import math
import datetime
from dataclasses import fields, is_dataclass
from typing import Dict, Any

_NON_GENERIC_TYPES = (str, int, float, bool, type(None))


def _serialize_non_generic_type(data):
    if isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
        return None
    if isinstance(data, datetime.datetime):
        return data.isoformat()
    return data


def _serialize_list(data):
    return [_serialize_data(item) for item in data]


def _serialize_dict(data):
    return {_serialize_data(k): _serialize_data(v) for k, v in data.items()}


def _serialize_dataclass(data):
    data_fields = fields(data)
    obj = {}
    for field in data_fields:
        value = _serialize_data(getattr(data, field.name))
        obj[field.name] = value
    return obj


def _serialize_data(data):
    if isinstance(data, _NON_GENERIC_TYPES):
        return data
    if isinstance(data, list):
        return _serialize_list(data)
    if isinstance(data, dict):
        return _serialize_dict(data)
    if is_dataclass(data):
        return _serialize_dataclass(data)
    raise ValueError(f"Cannot serialize '{data.__class__.__name__}' to JSON")


def serialize(data) -> Dict[str, Any]:
    if not is_dataclass(data):
        raise ValueError(
            f"Type '{data.__class__.__name__}' is not a dataclass")
    return _serialize_data(data)
