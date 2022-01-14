from dataclasses import dataclass
from typing import Dict

from .field import Field
from .helpers import get_available_countries


@dataclass
class Phone:
    phone: str = None

    def __init__(self, **kwargs):
        self.phone = kwargs.pop("phone", None)
        self.country_code = kwargs.pop("country_code", None)

    @property
    def country_code(self) -> str:
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

    def __str__(self) -> str:
        country_code = "({}) ".format(self.country_code) if self.country_code else ""
        return "{}{}".format(country_code, self.phone)


class PhoneField(Field):
    __monday_field_type__ = "phone"

    def __init__(self, *args, **kwargs):
        self.value: Phone = Phone(*args, **kwargs)

    def to_monday_dict(self):
        return (
            {
                "phone": self.value.phone,
                "countryShortName": self.value.country_code,
            }
            if self.value
            else {}
        )

    def from_monday_dict(self, data: Dict[str, str]):
        self.value.phone = data["phone"] if data else None
        self.value.country_code = data["countryShortName"] if data else None
