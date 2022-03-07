# KeepActionsAlive

Automatically prevent your scheduled GitHub Actions from becoming disabled after 60 days.

## Overview

This package is meant to be deployed in an AWS environment.
It contains a Lambda function which will run every `20 days`.
The Lambda function gets GitHub repositories belonging to an organization and hits the [enable workflow](https://docs.github.com/en/rest/reference/actions#enable-a-workflow) REST endpoint to re-enable the GitHub Actions workflow of each repository.
Additionally, you can re-enable workflows for a repository outside of your organization by modifying the `src/repos.config` file with a list of `GitHub_Organization/Repository_Name` entries.
## Installation

### Pre-Requisites

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

### Generate GitHub Personal Access Token

You will need a [personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) with a `workflow` scope.
You will then need to store your PAT in AWS SecretsManager.
To do so, replace `<foobar>` in the following command with the PAT you created above:

```bash
aws secretsmanager create-secret --name KeepActionsAlivePAT --secret-string '{"PAT": "<foobar>"}'
```

Copy the ARN of the created secret as you will need it when deploying the template next.

### Launch the Project

There are three parameters used when deploying the template:
- `PATSecretARN`: Enter the ARN from the secret for your PAT from the previous step
- `Organization`: Name of the GitHub organization which you want to re-enable workflows
- `UseExternalRepos`: If you have repositories outside of your organization which you wish to re-enable, this will look in the `src/repos.config` file for repos to enable (only `true/false` values allowed)


```bash
sam build --use-container
sam deploy --guided
```

## Cleanup


If you decide you no longer want to use the application, simply run:

```bash
aws cloudformation delete-stack --stack-name KeepActionsAlive  # Note: This needs to match what you entered in the `sam deploy` command
aws secretsmanager delete-secret --secret-id KeepActionsAlivePAT
```
