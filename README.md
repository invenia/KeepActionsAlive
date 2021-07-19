# KeepActionsAlive
Automatically prevent your scheduled GitHub Actions from becoming disabled after 60 days.

## Overview
This package is meant to be run on Amazon Web Services (AWS).
You will store a Personal Access Token (PAT) in SecretsManager.
Lambda will retrieve this token, and use it to make authenticated requests to the [enable workflow](https://docs.github.com/en/rest/reference/actions#enable-a-workflow) REST endpoint on GitHub.

When you launch the CloudFormation template you will be ask to input an organization where all repositories will be enabled.

TODO: Explain how non-organization projects can be added to a list for re-enabling
### Architecture Diagram
![Architecture](imgs/arch.png)
## Setup
The first step to using this repository is to generate a [personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) with a `workflow` scope.

TODO: Fill in how to launch the CloudFormation Template
TODO: Instructions on modifying the optional configuration for non-organization repos
