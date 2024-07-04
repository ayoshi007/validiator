from dataclasses import is_dataclass, fields
import math
import datetime


def serialize(data):
    if not is_dataclass(data):
        raise ValueError("Data must be a dataclass to serialize")
    obj_fields = fields(data)
