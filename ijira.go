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

func getEnvVars() (string, string, string) {
	username := os.Getenv("JIRA_USERNAME")
	password := os.Getenv("JIRA_PASSWORD")
	server := os.Getenv("JIRA_SERVER")
	project := os.Getenv("JIRA_PROJECT")

	if username == "" {
		fmt.Println("Error: JIRA_USERNAME environment variable is not set")
		os.Exit(1)
	}

	if password == "" {
		fmt.Println("Error: JIRA_PASSWORD environment variable is not set")
		os.Exit(1)
	}

	if server == "" {
		fmt.Println("Error: JIRA_SERVER environment variable is not set")
		os.Exit(1)
	}

	if project == "" {
		fmt.Println("Error: JIRA_PROJECT environment variable is not set")
	}

	return username, password, server, project
}

func main() {
	var opts Options
	_, err := flags.Parse(&opts)
	if err != nil {
		os.Exit(1)
	}

	username, password, server, project := getEnvVars()

	tp := jira.BasicAuthTransport{
		Username: username,
		Password: password,
	}

	client, err := jira.NewClient(tp.Client(), server)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	i := jira.Issue{
		Fields: &jira.IssueFields{
			Assignee: &jira.User{
				Name: opts.Assignee,
			},
			Summary: opts.Summary,
			Description: opts.Description,
			Type: jira.IssueType{
				Name: "Story",
			},
			Project: jira.Project{
				Key: project,
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