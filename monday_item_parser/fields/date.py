from collections import OrderedDict
from datetime import datetime
from typing import Dict

from .field import Field


class DateField(Field):
    __monday_field_type__ = "date"

    def __init__(self, default: datetime = None, include_time: bool = True):
        self.value = default
        self._include_time = include_time

    def to_monday_dict(self):
        data = (
            {
                "date": self.value.strftime("%Y-%m-%d"),
                "time": self.value.strftime("%H:%M:%S"),
            }
            if self.value
            else {}
        )

        if not self._include_time and "time" in data:
            del data["time"]

        return data

    def from_monday_dict(self, data: Dict[str, str]):
        if not data:
            self.value = None
            return

        variables = OrderedDict()
        time_format = OrderedDict()

        # Create the needed formatting only for the items that we have in the dictionary
        for key, time_fmt in {"date": "%Y-%m-%d", "time": "%H:%M:%S"}.items():
            if key not in data:
                continue

            variables[key] = data[key]
            time_format[key] = time_fmt

        # Parse the date & time by the formatting
        self.value = datetime.strptime(
            " ".join("{{{}}}".format(key) for key in variables).format(**variables),
            " ".join("{}".format(time_format[fmt]) for fmt in time_format),
        )

    def search_representation(self) -> str:
        return self.value.strftime("%Y-%m-%d")

    def __str__(self):
        format = "%Y-%m-%d"
        if self._include_time:
            format += " %H:%M:%S"

        return self.value.strftime(format) if self.value else str(None)
