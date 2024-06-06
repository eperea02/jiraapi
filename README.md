This is a cli for the Jira API to easily create issues.

To run this script copy the `run_ijira` bash script to your EC directory.

Then export these variables:

```shell
    export JIRA_USERNAME=<jira_username>
    export JIRA_PASSWORD=<jira_password>
```

Then running: `./run_ijira --help should show the correct output`

```shell
└─⭘ ./run_ijira create --help
usage: ijira create [-h] --summary SUMMARY [--description DESCRIPTION] [--labels {ktbr,ags-cli,common-tools,cef}] --assignee ASSIGNEE [--story-points STORY_POINTS]

optional arguments:
  -h, --help            show this help message and exit
  --summary SUMMARY     Issue summary
  --description DESCRIPTION
                        Issue description - will default to summary if not provided
  --labels {ktbr,ags-cli,common-tools,cef}
                        Issue labels
  --assignee ASSIGNEE   Assignee username
  --story-points STORY_POINTS
                        Story Points to assign to the task
```

Optional environment variables to set are listed in the `.env.example` file.

To request more label options please submit a merge request for this file [here](https://github.com/eperea02/jiraapi/blob/main/utils/labels.py#L9)
