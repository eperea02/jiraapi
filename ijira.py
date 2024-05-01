#! /usr/bin/env python
import pdb

from dotenv import load_dotenv

from utils.api import create_jira_issue, get_jira_instance, show_my_current_issues
from utils.arg_parser import get_parser
from utils.consts import project, token


def main():
    if not token:
        raise Exception("Token not configured")

    parser = get_parser()
    args = parser.parse_args()

    jira = get_jira_instance()
    if args.command == "create":
        create_jira_issue(
            jira,
            project,
            args.summary,
            args.description,
            args.labels,
            args.assignee,
        )
    elif args.command == "show":
        show_my_current_issues(jira, args.username)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
