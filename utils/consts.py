import os

server = os.getenv("JIRA_SERVER", "https://jira.devtools.intel.com/")
username = os.getenv("JIRA_USERNAME", "eperea")
token = os.getenv("JIRA_TOKEN", False)
password = os.getenv("JIRA_PASSWORD", False)
project = os.getenv("JIRA_PROJECT", "TWC4558")


label_mapping = {
    "ktbr": {
        "labels": ["ktbr", "2024-q2-ktbr"],
        "epic": "TWCP155-112",
    },
    "ags-cli": {
        "labels": ["ags-cli", "2024-q2-ecagscli"],
        "epic": "TWCP155-119",
    },
    "common-tools": {
        "labels": ["common-tools", "2024-q2-common-tools"],
        "epic": "TWCP155-112",
    },
}
