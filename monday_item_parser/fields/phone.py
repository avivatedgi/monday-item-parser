from typing import Dict
from .field import Field
from .helpers import get_available_countries


class PhoneField(Field):
    __monday_field_type__ = "phone"

    def __init__(self, default: str = None, country_code: str = None):
        self.value = default
        self.country_code = country_code

    @property
    def country_code(self):
        return self._country_code

    @country_code.setter
    def country_code(self, country_code: str):
        if not country_code:
            self._country_code = None
            return

        countries = get_available_countries()
        if country_code not in countries:
            raise ValueError(
                "Invalid country id, choose from ({})".format(", ".join(countries))
            )

        self._country_code = country_code

    def to_monday_dict(self):
        return (
            {
                "phone": self.value,
                "countryShortName": self.country_code,
            }
            if self.value
            else {}
        )

    def from_monday_dict(self, data: Dict[str, str]):
        self.value = data["phone"] if data else None
        self.country_code = data["countryShortName"] if data else None

    def __str__(self):
        country_code = " ({})".format(self.country_code)
        return "{}{}".format(self.value, country_code if country_code else "")
