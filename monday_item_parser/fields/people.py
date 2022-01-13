from typing import List, Union, Dict

from .field import Field


class Person:
    def __init__(self, id: int):
        self.id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def kind(self):
        return "person"


class Team:
    def __init__(self, id: int):
        self.id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def kind(self):
        return "team"


class PeopleField(Field):
    __monday_field_type__ = "multiple-person"

    def __init__(self, default: List[Union[Person, Team]] = []):
        self.value = default

    def to_monday_dict(self):
        return (
            {"personsAndTeams": [{"id": x.id, "kind": x.kind} for x in self.value]}
            if self.value
            else {}
        )

    def from_monday_dict(self, data: Dict[str, str]):
        if not data:
            return

        value = []

        for people in data["personsAndTeams"]:
            if people["kind"] == "person":
                value.append(Person(people["id"]))
            elif people["kind"] == "team":
                value.append(Team(people["id"]))

        self.value = value

    def __str__(self):
        attrs = (
            ", ".join("{}: {}".format(x.kind, x.id) for x in self.value)
            if self.value
            else ""
        )

        return f"[{attrs}]"
