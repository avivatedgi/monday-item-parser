from typing import Any, Dict

from .field import Field
from .helpers import get_available_countries


class CountryField(Field):
    __monday_field_type__ = "country"

    def __init__(self, default: str = None):
        self.value = default

    def to_monday_dict(self):
        return {
            "countryCode": self.value,
            "countryName": self.value,
        }

    def from_monday_dict(self, data: Dict[str, Any]):
        self.value = data["countryCode"] if data else None

    @Field.value.setter
    def value(self, country_code: str):
        if not country_code:
            self._value = None
            return

        countries = get_available_countries()
        if country_code not in countries:
            raise ValueError(
                "Invalid country id, choose from ({})".format(", ".join(countries))
            )

        self._value = country_code
