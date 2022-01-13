from typing import Dict

from .field import Field


class EmailField(Field):
    __monday_field_type__ = "email"

    def __init__(self, default: str = None):
        self.value = default

    def to_monday_dict(self):
        return {"email": self.value, "text": self.value}

    def from_monday_dict(self, data: Dict[str, str]):
        self.value = data["email"] if data else None
