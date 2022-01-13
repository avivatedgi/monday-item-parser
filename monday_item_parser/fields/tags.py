from typing import Any, Dict, List

from .field import Field


class TagsField(Field):
    __monday_field_type__ = "tag"

    def __init__(self, default: List[int] = []):
        self.value = default

    def to_monday_dict(self):
        return {"tag_ids": self.value}

    def from_monday_dict(self, data: Dict[str, Any]):
        self.value = data["tag_ids"] if data else None
