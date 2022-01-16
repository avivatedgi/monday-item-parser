from typing import Any, Dict, Union

from .field import Field


class StatusField(Field):
    __monday_field_type__ = "color"
    __type_to_field_name__ = {str: "label", int: "index"}

    def __init__(self, value: Union[str, int] = None):
        self.value = value

    def to_monday_dict(self):
        return (
            {StatusField.__type_to_field_name__[type(self.value)]: self.value}
            if self.value
            else None
        )

    def from_monday_dict(self, data: Dict[str, Any]):
        if not data:
            self.value = None
            return

        for key in StatusField.__type_to_field_name__.values():
            if key in data:
                self.value = data[key]
                break
        else:
            self.value = None

    def __str__(self):
        if self.value is None:
            return str(None)

        field_name = StatusField.__type_to_field_name__[type(self.value)]
        return f"{field_name}: {self.value}"

    def search_representation(self) -> str:
        if not self.value:
            raise ValueError("Can not search statuses by empty value")
        elif isinstance(self.value, int):
            raise TypeError("Can not search statuses by indexes, only by labels")

        return str(self.value)
