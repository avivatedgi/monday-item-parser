from typing import Dict

from .field import Field


class MirrorField(Field):
    __monday_field_type__ = "lookup"
    __use_text_instead_of_value__ = True

    def __init__(self, default: str = None):
        self.value = default

    def to_monday_dict(self):
        return self.value

    def from_monday_dict(self, data: str):
        self.value = data if data else None

    def search_representation(self) -> str:
        return str(self.value)
