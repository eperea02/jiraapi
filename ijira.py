import argparse
import os
import pdb
from pprint import pp

from dotenv import load_dotenv
from jira import JIRA, JIRAError


def create_jira_issue(
    jira,
    project_key,
    summary,
    description,
    labels,
    assignee,
):
    try:
        issue_dict = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Story"},
            "labels": labels,
            "assignee": {"name": assignee},
        }

        issue = jira.create_issue(issue_dict)
        print(f"Issue {issue.key} created successfully in project {project_key}")
    except Exception as e:
        pp(e)


def main():
    load_dotenv()
    server = os.getenv("JIRA_SERVER", "https://jira.devtools.intel.com/")
    username = os.getenv("JIRA_USERNAME", "eperea")
    token = os.getenv("JIRA_TOKEN", False)
    password = os.getenv("JIRA_PASSWORD", False)
    project = os.getenv("JIRA_PROJECT", "TWC4558")
    if not token:
        raise Exception("Token not configured")

    parser = argparse.ArgumentParser(description="JIRA operations.")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a JIRA issue.")
    create_parser.add_argument("--summary", required=True, help="Issue summary")
    create_parser.add_argument("--description", required=True, help="Issue description")
    create_parser.add_argument("--labels", nargs="+", help="Issue labels")
    create_parser.add_argument("--assignee", required=True, help="Assignee username")

    args = parser.parse_args()
    jira = JIRA(
        basic_auth=(username, password),
        options={
            "server": server,
            "verify": "/etc/ssl/certs/ca-certificates.crt",
        },
    )

    if args.command == "create":
        create_jira_issue(
            jira,
            project,
            args.summary,
            args.description,
            args.labels,
            args.assignee,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
