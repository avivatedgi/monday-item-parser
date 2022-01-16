import inspect

from .exceptions import MondayClientError


def as_type(obj):
    return obj if inspect.isclass(obj) else type(obj)


def as_obj(obj):
    return obj if not inspect.isclass(obj) else obj()


def raise_monday_errors(response):
    if isinstance(response, dict) and "errors" in response:
        errors = [
            error["message"] if "message" in error else error
            for error in response["errors"]
        ]

        raise MondayClientError("Got error from monday client", errors)
