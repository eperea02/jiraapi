import os
import sys

from dotenv import load_dotenv

from utils.quarter import get_current_quarter

if os.path.exists(".env"):
    load_dotenv()
else:
    print("Warning: the .env file was not found.")
    print("Please ensure it exists and try again.")
    print(
        "Take a look at the .env.example file for an example of what needs to be provided."
    )
    sys.exit(1)


server = os.getenv("JIRA_SERVER", "https://jira.devtools.intel.com/")
username = os.getenv("JIRA_USERNAME", "eperea")
token = os.getenv("JIRA_TOKEN", False)
password = os.getenv("JIRA_PASSWORD", False)
project = os.getenv("JIRA_PROJECT", "TWC4558")
board_id = os.getenv("JIRA_BOARD_ID", "39982")
quarter = get_current_quarter()

label_mapping = {
    "ktbr": {
        "labels": ["ktbr", f"2024-q{quarter}-ktbr"],
        "epic": "TWCP155-112",
    },
    "ags-cli": {
        "labels": ["ags-cli", f"2024-q{quarter}-ecagscli"],
        "epic": "TWCP155-119",
    },
    "common-tools": {
        "labels": ["common-tools", f"2024-q{quarter}-common-tools"],
        "epic": "TWCP155-112",
    },
    "cef": {
        "labels": [
            "cef",
            "customer-engagement-forum",
            f"2024-q{quarter}-customer-engagement-forum",
        ],
        "epic": "TWCP155-112",
    },
}
