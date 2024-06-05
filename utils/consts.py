import os
import sys
from datetime import datetime

from dotenv import load_dotenv

from utils.labels import labels

load_dotenv()


def check_env_vars():
    vars_to_check = ["JIRA_USERNAME", "JIRA_PASSWORD"]
    result = True
    for var in vars_to_check:
        if os.getenv(var) is None:
            print(f"Error: The {var} environment variable is not set.")
            result = False

    return result


if not check_env_vars():
    sys.exit(2)


server = os.getenv("JIRA_SERVER", "https://jira.devtools.intel.com/")
username = os.getenv("JIRA_USERNAME", "eperea")
password = os.getenv("JIRA_PASSWORD", False)
project = os.getenv("JIRA_PROJECT", "TWC4558")
board_id = os.getenv("JIRA_BOARD_ID", "39982")
label_mapping = labels
