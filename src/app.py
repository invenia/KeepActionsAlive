from github import Github
import boto3
import json
import os
import requests


def get_params():
    """
    Retrieve environment variables
    """
    pat_name = os.getenv("PAT_SECRET_NAME")
    pat = get_pat(pat_name)

    organization = os.getenv("GH_ORGANIZATION")
    external_repos = os.getenv("EXTERNAL_REPOS")

    return pat, organization, external_repos


def get_pat(pat_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=pat_name)
    secret_string = json.loads(response["SecretString"])

    return secret_string["PAT"]


def get_repos(gh, organization, external_repos):
    """
    Get all repos for an organization, and external repos from the config file if the
    ENV VAR was set.
    """
    repos = []

    org_repos = gh.get_organization(organization).get_repos()
    valid_repos = [r for r in org_repos if not r.fork and not r.archived]
    repos += valid_repos

    if external_repos:
        external_repos = get_external_repos(gh)
        repos += external_repos

    return repos


def get_external_repos(gh):
    """
    Get all external repositories from the `repos.config` file
    """
    external_repos = []

    with open("repos.config") as f:
        content = f.readlines()
        content = [x.strip() for x in content]

        for entry in content:
            org_name, repo_name = entry.split('/')

            external_repos.append(gh.get_organization(org_name).get_repo(repo_name))

    return external_repos


def get_workflows(repos):
    """
    Get all the workflows with a `disabled_inactivity` state.
    """
    disabled_workflows = []

    for repo in repos:
        workflows_to_enable = [
            w for w in repo.get_workflows() if w.state == "disabled_inactivity"
        ]

        disabled_workflows += workflows_to_enable

    return disabled_workflows


def enable_workflows(pat, workflows):
    """
    Enable all the workflows.
    """
    for workflow in workflows:
        enable_url = f"{workflow.url}/enable"
        header = {"Authorization": f"Bearer {pat}"}
        requests.put(enable_url, headers=header)


def lambda_handler(event, context):
    """
    Enable all inactive workflows.
    """
    pat, organization, external_repos = get_params()

    gh = Github(login_or_token=pat)

    repos = get_repos(gh, organization, external_repos)
    workflows = get_workflows(repos)
    enable_workflows(pat, workflows)

    return {"statusCode": 200}
