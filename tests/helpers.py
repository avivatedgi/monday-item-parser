import os
import time

from typing import Optional
from monday import MondayClient
from monday_item_parser import MondayClientError

client = MondayClient(os.environ.get("MONDAY_API_KEY"))

testing_board_id = int(os.environ.get("MONDAY_TESTING_BOARD_ID"))


def is_budget_exhausted_in_exception(exc: MondayClientError) -> Optional[int]:
    errors = exc.args[1]
    for error in errors:
        if "Complexity budget exhausted" in error:
            time_to_wait = int(error.split(" ")[-2])
            return time_to_wait

    return None


def retry_in_case_of_budget_exhausted(func):
    try:
        return func()
    except MondayClientError as exc:
        time_to_wait = is_budget_exhausted_in_exception(exc)
        if time_to_wait is not None:
            time.sleep(time_to_wait)
            return retry_in_case_of_budget_exhausted(func)
