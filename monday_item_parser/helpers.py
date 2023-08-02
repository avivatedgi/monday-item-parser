import inspect

from .exceptions import MondayClientError


def as_type(obj):
    return obj if inspect.isclass(obj) else type(obj)


def as_obj(obj):
    return obj if not inspect.isclass(obj) else obj()


def remove_none_from_dict(data):
    return {k: v for k, v in data.items() if v is not None} if isinstance(data, dict) else data

def raise_monday_errors(response):
    if isinstance(response, dict) and "errors" in response:
        errors = [error["message"] if "message" in error else error for error in response["errors"]]

        raise MondayClientError("Got error from monday client", errors)
