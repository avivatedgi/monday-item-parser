from typing import Any, Dict

from .field import Field


class LinkField(Field):
    __monday_field_type__ = "link"

    def __init__(self, default: str = None, text: str = None):
        self.value = default
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    def to_monday_dict(self):
        return {"url": self.value, "text": self.text} if self.value else {}

    def from_monday_dict(self, data: Dict[str, Any]):
        self.value = data["url"] if data else None
        self.text = data["text"] if data else None
