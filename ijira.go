package main

import (
	"fmt"
	"github.com/andygrunwald/go-jira"
	"github.com/jessevdk/go-flags"
	"os"
)

type Options struct {
	Summary     string   `short:"s" long:"summary" description:"Issue summary" required:"true"`
	Description string   `short:"d" long:"description" description:"Issue description" required:"true"`
	Labels      []string `short:"l" long:"labels" description:"Issue labels"`
	Assignee    string   `short:"a" long:"assignee" description:"Assignee username" required:"true"`
}

func main() {
	var opts Options
	_, err := flags.Parse(&opts)
	if err != nil {
		panic(err)
	}

	tp := jira.BasicAuthTransport{
		Username: os.Getenv("JIRA_USERNAME"),
		Password: os.Getenv("JIRA_PASSWORD"),
	}

	client, err := jira.NewClient(tp.Client(), os.Getenv("JIRA_SERVER"))
	if err != nil {
		panic(err)
	}

	i := jira.Issue{
		Fields: &jira.IssueFields{
			Assignee: &jira.User{
				Name: opts.Assignee,
			},
			Summary:     opts.Summary,
			Description: opts.Description,
			Type: jira.IssueType{
				Name: "Story",
			},
			Project: jira.Project{
				Key: os.Getenv("JIRA_PROJECT"),
			},
			Labels: opts.Labels,
		},
	}

	issue, _, err := client.Issue.Create(&i)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Issue %s created successfully in project %s\n", issue.Key, os.Getenv("JIRA_PROJECT"))
}