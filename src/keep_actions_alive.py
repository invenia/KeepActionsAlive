#!/usr/bin/env python

from github import Github
import os
import pprint
import requests


def get_parameters():
    # Get parameters from environment variables
    return {
        "login_or_token": os.getenv(
            "GH_LOGIN_OR_TOKEN"
        ),
        "organization": os.getenv("GH_ORGANIZATION"),
        "user": os.getenv("GH_USER"),
    }


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    parameters = get_parameters()

    login_or_token = parameters["login_or_token"]
    organization = parameters["organization"]
    user = parameters["user"]

    # Logic should be added here to support other authentication in the future
    auth = (user, login_or_token) if user else None
    g = Github(login_or_token=login_or_token)

    # Get all repos that are not forks and are not archived
    # Only supports repos owned by an organization for now
    repos = g.get_organization(organization).get_repos()
    owned_repos = [r for r in repos if not r.fork and not r.archived]

    for repo in owned_repos:
        # Get all workflows disabled from inactivity
        disabled_workflows = [
            w for w in repo.get_workflows() if w.state == "disabled_inactivity"
        ]

        if auth:  # Not tested yet
            for workflow in disabled_workflows:
                enable_url = f"{workflow.url}/enable"
                requests.put(enable_url, auth=auth)
        else:
            print(disabled_workflows)
