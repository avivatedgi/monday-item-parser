from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from .field import Field


@dataclass
class Timeline:
    start: datetime = None
    end: datetime = None

    def __str__(self):
        return "{} -> {}".format(
            self.start.strftime("%Y-%m-%d"),
            self.end.strftime("%Y-%m-%d"),
        )


class TimelineField(Field):
    __monday_field_type__ = "timerange"

    def __init__(self, *args, **kwargs):
        self.value: Timeline = Timeline(*args, **kwargs)

    def to_monday_dict(self):
        return (
            {
                "from": self.value.start.strftime("%Y-%m-%d"),
                "to": self.value.end.strftime("%Y-%m-%d"),
            }
            if self.value and self.value.start and self.value.end
            else {}
        )

    def from_monday_dict(self, data: Dict[str, str]):
        if not data:
            self.value = None
            return

        self.value = Timeline(
            start=datetime.strptime(data["from"], "%Y-%m-%d"),
            end=datetime.strptime(data["to"], "%Y-%m-%d"),
        )
