from github import Github
import os
import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)

login_or_token = os.getenv(
    "GH_LOGIN_OR_TOKEN"
)  # Passwords not supported in this implementation
organization = os.getenv("GH_ORGANIZATION")
user = os.getenv("GH_USER")


g = Github(login_or_token=login_or_token)

repos = g.get_organization(organization).get_repos()

# Get all repos that belong to Invenia and are not forks and are not archived
invenia_repos = [r for r in repos if not r.fork and not r.archived]

for repo in invenia_repos:
    disabled_workflows = [
        w for w in repo.get_workflows() if w.state == "disabled_inactivity"
    ]

    if user and login_or_token:  # Not tested yet
        for workflow in disabled_workflows:
            enable_url = f"{workflow.url}/enable"
            requests.put(enable_url, auth=(user, login_or_token))
    else:
        print(disabled_workflows)
