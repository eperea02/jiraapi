from pprint import pp

import pandas as pd
from jira import JIRA
from utils.consts import board_id, label_mapping, password, project, server, username


def get_jira_instance():
    return JIRA(
        basic_auth=(username, password),
        options={
            "server": server,
            "verify": "/etc/ssl/certs/ca-certificates.crt",
        },
    )


# Example jira issue in Rest API https://jira.devtools.intel.com/rest/api/2/issue/TWC4558-3339
def create_jira_issue(
    jira, summary, description, label, assignee, story_points, backlog
):
    try:
        labels = label_mapping.get(label).get("labels")
        epic_key = label_mapping.get(label).get("epic")

        issue_dict = {
            "project": {"key": project},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Story"},
            "labels": labels,
            "assignee": {"name": assignee},
            "customfield_11204": story_points,  # This is the story points
        }

        if not backlog:
            current_sprint = jira.sprints(board_id, state="active")[0]
            issue_dict["customfield_11605"] = (current_sprint.id,)

        issue = jira.create_issue(issue_dict)
        jira.add_issues_to_epic(epic_key, [issue.key])
        print(f"Issue {issue.key} created successfully in project {project}")
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
