from typing import Dict


_COUNTRIES = {}


def get_available_countries() -> Dict[str, str]:
    """
    This function loads the list of countries from http://country.io to support
    monday's fields that need country codes (like Country and Phone fields).
    """

    global _COUNTRIES
    if not _COUNTRIES:
        import json
        import requests

        response = requests.get("http://country.io/names.json")
        if response.status_code != 200:
            raise Exception(
                "Failed to fetch countries, status_code={}, response={}".format(
                    response.status_code, response.text
                )
            )

        _COUNTRIES = json.loads(response.text)

    # Make sure we return a copy instead of the global variable
    # so it won't be changed
    return dict(_COUNTRIES)
