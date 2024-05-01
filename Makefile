.DEFAULT_GOAL:=help


JIRAAPI := jiraapi

.PHONY: build run install


SHELL := /bin/bash

test: 						## Run Unit Tests
	@coverage run -m pytest

fixlf: 						## Lint/Format code and push to branch
	@make format
	@make fixlint

checkformat:				## Chceck formatting of code using black 
	black --check .

format:						## Format code using black
	black .

lint:						## Lint code using flake
	flake8 .

fixlint:					## Autofix linting with autoflake8
	autoflake8 -r -i  --exit-zero-even-if-changed --remove-duplicate-keys --remove-unused-variables .

docker:						## Build and run Docker Image
	make buildImage
	make runImage

buildImage: 				## Build Current Image
	@docker build ${BUILD_ARGS} -t ${JIRAAPI}:latest . 

runImage: 					## Build Current Image
	docker run -it -p 8000:8000 --env-file .env ${JIRAAPI}:latest 

rebuild:					## Rebuild and run Docker Image
	make buildImage
	make bindShell

shellDev:					## [Dev] - Bring up shell of devservice container for checking environment
	docker run -it --entrypoint /bin/bash --env-file .env -p 8000:8000 ${JIRAAPI}:latest

bindShell: 					## Bind do the docker shell
	docker run -it --entrypoint /bin/bash -v /$(shell pwd):/app --env-file .env  -p 8000:8000 ${JIRAAPI}:latest

install:					## Install the application into one file
	pyinstaller ./ijira.py --onefile --name ijira

testcreate:					## Test create command
	python ijira.py create --summary "test summary" --description "test description" --assignee eperea --labels "common-tools"

testshow:					## Test show command
	python ijira.py show --username eperea

tc: 
	make testcreate

ts: 
	make testshow

itest:						## Interactively test a command, will rerun command on save
	ptw --runner "pytest ./tests/test_query_request.py"

itestverbose:						## Interactively test a command, will rerun command on save
	ptw --runner "pytest -v -s ./tests/test_query_request.py"

help:						## Show this help.
	@echo "Jira CLI Build and Deployment Commands"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
