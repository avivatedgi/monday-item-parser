from dataclasses import dataclass
from typing import Any, Dict

from .field import Field


@dataclass
class Link:
    url: str = None
    text: str = None

    def __str__(self):
        return "{} ({})".format(self.text, self.url)


class LinkField(Field):
    __monday_field_type__ = "link"

    def __init__(self, *args, **kwargs):
        self.value: Link = Link(*args, **kwargs)

    def to_monday_dict(self):
        return {"url": self.value.url, "text": self.value.text} if self.value else {}

    def from_monday_dict(self, data: Dict[str, Any]):
        self.value.url = data["url"] if data else None
        self.value.text = data["text"] if data else None

    def search_representation(self) -> str:
        return str(self.value.text)
