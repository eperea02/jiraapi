.DEFAULT_GOAL:=help


JIRAAPI := jiracli

.PHONY: build run install


SHELL := /bin/bash
IJIRA_IMAGE_HARBOR := amr-registry.caas.intel.com/ec-fieldengineering/${JIRAAPI}:latest

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

buildTagAndPushImage: 		## Build Current Image and push it to harbor
	@docker build ${BUILD_ARGS} -t ${JIRAAPI}:latest . 
	@docker tag ${JIRAAPI}:latest ${IJIRA_IMAGE_HARBOR}
	@docker push ${IJIRA_IMAGE_HARBOR}

buildImage: 				## Build Current Image
	@docker build ${BUILD_ARGS} -t ${JIRAAPI}:latest . 

runImage: 					## Build Current Image
	@docker run -it -e JIRA_SERVER=${JIRA_SERVER} -e JIRA_USERNAME=${JIRA_USERNAME} -e JIRA_PASSWORD=${JIRA_PASSWORD} -e JIRA_PROJECT=${JIRA_PROJECT} -p 8000:8000 ${JIRAAPI}:latest 

rebuild:					## Rebuild and run Docker Image
	make buildImage
	make bindShell

jira: 						## run Image
	@if [ -z "$(ARGS)" ]; then echo "Please use ARGS to define arguments like ARGS=\"show --username eperea\""; exit 1; fi
	@if [ -z "$(shell docker images -q ${JIRAAPI}:latest)" ]; then echo "Docker image ${JIRAAPI}:latest does not exist. Please build the image first using 'make buildImage' or 'make buildUbuntu'"; exit 1; fi
	@docker run --env-file .env -it -p 8080:8080 ${JIRAAPI}:latest $(ARGS)


shellDev:					## [Dev] - Bring up shell of devservice container for checking environment
	docker run -it --entrypoint /bin/bash --env-file .env -p 8000:8000 ${JIRAAPI}:latest

bindShell: 					## Bind do the docker shell
	docker run -it --entrypoint /bin/bash -v /$(shell pwd):/app -p 8000:8000 ${JIRAAPI}:latest

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
