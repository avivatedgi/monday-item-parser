from dataclasses import dataclass
from typing import Self
from dataclasses_json import dataclass_json, LetterCase

from .field import Field
from ..helpers import remove_none_from_dict


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class City:
    long_name: str | None = None
    short_name: str | None = None

    def from_monday_dict(self, data: dict[str, str]):
        self.long_name = data.get("long_name", None) if data else None
        self.short_name = data.get("short_name", None) if data else None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Country:
    long_name: str | None = None
    short_name: str | None = None

    def from_monday_dict(self, data: dict[str, str]):
        self.long_name = data.get("long_name", None) if data else None
        self.short_name = data.get("short_name", None) if data else None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Location:
    address: str | None = None
    city: City | None = None
    country: Country | None = None
    lat: float | None = None
    lng: float | None = None
    place_id: str | None = None
    street: str | None = None
    street_short: str | None = None
    street_number: str | None = None
    street_number_short: str | None = None
    text: str | None = None

    def from_monday_dict(self, data: dict[str, str]) -> Self:
        self.address = data.get("address", None) if data else None
        self.city = City().from_monday_dict(data.get("city", None)) if data else None
        self.country = Country().from_monday_dict(data.get("country", None)) if data else None
        self.lat = float(data.get("lat", None)) if data else None
        self.lng = float(data.get("lng", None)) if data else None
        self.place_id = data.get("placeId", None) if data else None
        self.street = data.get("street", None) if data else None
        self.street_short = data.get("streetShort", None) if data else None
        self.street_number = data.get("streetNumber", None) if data else None
        self.street_number_short = data.get("streetNumberShort", None) if data else None
        self.text = data.get("text", None) if data else None
        return self

    def to_monday_dict(self) -> dict[str, str]:
        return {
            "address": self.address,
            "lat": self.lat,
            "lng": self.lng,
        }
    
    def __str__(self):
        return self.text if self.text else "None"


class LocationField(Field):
    __monday_field_type__ = "location"

    def __init__(self, *args, **kwargs):
        self.value: Location = Location(*args, **kwargs)

    def to_monday_dict(self) -> dict[str, str] | None:
        clear_data = remove_none_from_dict(self.value.to_monday_dict()) if self.value else None
        print(clear_data)
        return clear_data or None

    def from_monday_dict(self, data: dict[str, str]):
        self.value = Location().from_monday_dict(data) 

    def __str__(self):
        return str(self.value.address) if self.value and self.value.address else "None"
