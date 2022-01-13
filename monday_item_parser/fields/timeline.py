from datetime import datetime
from typing import Dict

from .field import Field


class TimelineField(Field):
    __monday_field_type__ = "timerange"

    def __init__(self, start: datetime = None, end: datetime = None):
        self.value = [start, end] if start and end else None

    def to_monday_dict(self):
        return (
            {
                "from": self.value[0].strftime("%Y-%m-%d"),
                "to": self.value[1].strftime("%Y-%m-%d"),
            }
            if self.value
            else {}
        )

    def from_monday_dict(self, data: Dict[str, str]):
        self.value = (
            [
                datetime.strptime(
                    "{date}".format(date=data[key]),
                    "%Y-%m-%d",
                )
                for key in ("from", "to")
            ]
            if data
            else None
        )

    def __str__(self):
        return "from: {}, to: {}".format(*self.value) if self.value else ""

    @Field.value.setter
    def value(self, value):
        if not value:
            self._value = value
            return

        if not isinstance(value, list) or any(
            not isinstance(x, datetime) for x in value
        ):
            raise TypeError("{} can only accept list of datetime objects!")

        if len(value) != 2:
            raise AttributeError("Timeline must have start and end date objects")

        self._value = value
