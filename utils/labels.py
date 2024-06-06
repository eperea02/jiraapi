from datetime import datetime

from utils.quarter import get_current_quarter

quarter = get_current_quarter()
current_year = datetime.now().year


labels = {
    "ktbr": {
        "labels": ["ktbr", f"{current_year}-q{quarter}-ktbr"],
        "epic": "TWCP155-112",
    },
    "ags-cli": {
        "labels": ["ags-cli", f"{current_year}-q{quarter}-ecagscli"],
        "epic": "TWCP155-119",
    },
    "common-tools": {
        "labels": ["common-tools", f"{current_year}-q{quarter}-common-tools"],
        "epic": "TWCP155-112",
    },
    "cef": {
        "labels": [
            "cef",
            "customer-engagement-forum",
            f"{current_year}-q{quarter}-customer-engagement-forum",
        ],
        "epic": "TWCP155-112",
    },
    "pe": {
        "labels": [
            "ec-pe",
            "ec-project-enablement",
            f"{current_year}-q{quarter}-project-enablement",
            f"{current_year}-q{quarter}-project_enablement",
        ],
        "epic": "TWCP155-122",
    },
    "autodebug": {
        "labels": [
            "autodebug",
            "autodebugapi",
            f"{current_year}-q{quarter}-autodebug",
        ],
        "epic": "TWCP155-120",
    },
}
