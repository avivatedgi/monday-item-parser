import os

from monday import MondayClient


client = MondayClient(os.environ.get("MONDAY_API_KEY"))

testing_board_id = int(os.environ.get("MONDAY_TESTING_BOARD_ID"))
