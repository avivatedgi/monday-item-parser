from collections import OrderedDict
from datetime import datetime
from typing import Dict

from .field import Field


class DateField(Field):
    __monday_field_type__ = "date"

    def __init__(self, default: datetime = None):
        self.value = default

    def to_monday_dict(self):
        return (
            {
                "date": self.value.strftime("%Y-%m-%d"),
                "time": self.value.strftime("%H:%M:%S"),
            }
            if self.value
            else {}
        )

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

    def __str__(self):
        return self.value.strftime("%Y-%m-%d %H:%M:%S") if self.value else str(None)
