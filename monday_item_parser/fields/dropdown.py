from typing import Any, Dict, List

from .field import Field


class DropdownField(Field):
    __monday_field_type__ = "dropdown"

    def __init__(self, default: List[str] = []):
        self.value = default
        self._by = "labels"

    def to_monday_dict(self):
        if self._by == "ids":
            return {"ids": self._ids}

        return {"labels": self.value} if self.value else None

    def from_monday_dict(self, data: Dict[str, Any]):
        if data:
            self._by = "ids"
            self.value = [int(x) for x in data["ids"]]
