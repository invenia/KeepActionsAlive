#!/usr/bin/env python

from github import Github
import os
import pprint
import requests

IS_LAMBDA = bool(os.getenv("AWS_EXECUTION_ENV"))


def get_parameters():
    # Add more options for adding arguments here,
    # such as CLI args, AWS Secrets Manager, config file, etc.

    # Get keyword arguments from environment variables
    return {
        "login_or_token": os.getenv("GH_LOGIN_OR_TOKEN"),
        "organization": os.getenv("GH_ORGANIZATION"),
    }


def keep_actions_alive(parameters):
    pp = pprint.PrettyPrinter(indent=4)

    login_or_token = parameters["login_or_token"]
    organization = parameters["organization"]

    g = Github(login_or_token=login_or_token)

    # Get all repos that are not forks and are not archived
    # Only supports repos owned by an organization for now,
    # but could be changed to users
    repos = g.get_organization(organization).get_repos()
    owned_repos = [r for r in repos if not r.fork and not r.archived]

    for repo in owned_repos:
        # Get all workflows disabled from inactivity
        disabled_workflows = [
            w for w in repo.get_workflows() if w.state == "disabled_inactivity"
        ]

        if login_or_token:  # Use token authentication
            for workflow in disabled_workflows:
                # There's no  documented pygithub API call for enabling the
                # workflow, so the rest API should work here
                enable_url = f"{workflow.url}/enable"
                token_header = {"Authorization": f"Bearer {login_or_token}"}
                requests.put(enable_url, headers=token_header)
        else:
            # No authentication, so just output the disabled workflows
            pp.pprint(disabled_workflows)


if __name__ == "__main__":
    parameters = get_parameters()
    keep_actions_alive(parameters)
