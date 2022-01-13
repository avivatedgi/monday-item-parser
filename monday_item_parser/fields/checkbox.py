from typing import Any, Dict

from .field import Field


class CheckboxField(Field):
    __monday_field_type__ = "boolean"

    def __init__(self, default: bool = False):
        self.value = default

    def to_monday_dict(self):
        return {"checked": "true"} if self.value else {}

    def from_monday_dict(self, data: Dict[str, Any]):
        self.value = data["checked"] if data else False
