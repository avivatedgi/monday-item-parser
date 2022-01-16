import os
import time

from monday import MondayClient
from monday_item_parser import MondayClientError

client = MondayClient(os.environ.get("MONDAY_API_KEY"))

testing_board_id = int(os.environ.get("MONDAY_TESTING_BOARD_ID"))


def retry_in_case_of_budget_exhausted(func):
    try:
        return func()
    except MondayClientError as exc:
        errors = exc.args[1]
        for error in errors:
            if "Complexity budget exhausted" in error:
                time_to_wait = int(error.split(" ")[-2])
                time.sleep(time_to_wait)
                return retry_in_case_of_budget_exhausted(func)
