from typing import Dict

from .field import Field


class TextField(Field):
    __monday_field_type__ = "text"

    def __init__(self, default: str = None):
        self.value = default

    def to_monday_dict(self):
        return self.value

    def from_monday_dict(self, data: str):
        self.value = data if data else None

    def search_representation(self) -> str:
        return str(self.value)


class LongTextField(Field):
    __monday_field_type__ = "long-text"

    def __init__(self, default: str = None):
        self.value = default

    def to_monday_dict(self):
        return {"text": self.value}

    def from_monday_dict(self, data: str):
        self.value = data if data else None

    def search_representation(self) -> str:
        return str(self.value)
