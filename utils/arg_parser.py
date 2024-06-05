import argparse

from utils.consts import label_mapping


def get_parser():
    parser = argparse.ArgumentParser(description="JIRA operations.")
    subparsers = parser.add_subparsers(dest="command")

    create_sub_parser(subparsers)
    show_sub_parser(subparsers)
    return parser


def create_sub_parser(subparsers):
    labels = [label for label in label_mapping.keys()]
    create_parser = subparsers.add_parser("create", help="Create a JIRA issue.")
    create_parser.add_argument("--summary", required=True, help="Issue summary")
    create_parser.add_argument(
        "--description",
        help="Issue description - will default to summary if not provided",
    )
    create_parser.add_argument("--labels", choices=labels, help="Issue labels")
    create_parser.add_argument("--assignee", required=True, help="Assignee username")
    create_parser.add_argument(
        "--story-points", default=1, type=int, help="Story Points to assign to the task"
    )


def show_sub_parser(subparsers):
    show_parser = subparsers.add_parser("show", help="Show my current issues.")
    show_parser.add_argument(
        "--username", required=True, help="Show issues for this user."
    )
