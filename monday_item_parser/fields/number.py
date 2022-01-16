import json

from typing import Union

from .field import Field


class NumberField(Field):
    __monday_field_type__ = "numeric"

    def __init__(self, default: Union[int, float] = None):
        self.value = default

    def to_monday_dict(self):
        return str(self.value) if self.value is not None else None

    def from_monday_dict(self, data: Union[int, float]):
        self.value = json.loads(data) if data else None

    def search_representation(self) -> str:
        return str(self.value)
