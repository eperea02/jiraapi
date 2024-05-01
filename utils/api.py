from pprint import pp

import pandas as pd
from jira import JIRA

from utils.consts import label_mapping, password, server, username


def get_jira_instance():
    return JIRA(
        basic_auth=(username, password),
        options={
            "server": server,
            "verify": "/etc/ssl/certs/ca-certificates.crt",
        },
    )


def create_jira_issue(
    jira,
    project_key,
    summary,
    description,
    label,
    assignee,
):
    try:
        labels = label_mapping.get(label).get("labels")
        epic_key = label_mapping.get(label).get("epic")
        issue_dict = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Story"},
            "labels": labels,
            "assignee": {"name": assignee},
        }

        issue = jira.create_issue(issue_dict)
        jira.add_issues_to_epic(epic_key, [issue.key])
        print(f"Issue {issue.key} created successfully in project {project_key}")
    except Exception as e:
        pp(e)


def show_my_current_issues(jira, username):
    jql = f'assignee = {username} AND status in ("TO DO", "Defined", "In Progress")'
    issues = jira.search_issues(jql)
    issues_dict_list = []
    for issue in issues:
        issue_dict = {
            "Key": issue.key,
            "Summary": issue.fields.summary,
            "Status": issue.fields.status.name,
            # Add more fields as needed
        }
        issues_dict_list.append(issue_dict)
    df = pd.DataFrame(issues_dict_list)
    print(df.to_markdown(tablefmt="grid", index=False))


# Usage
