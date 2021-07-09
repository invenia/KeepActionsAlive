from github import Github
import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)

name = "mattBrzezinski"
pat = "redacted"

g = Github(pat)

repos = g.get_user().get_repos()

# Get all repos that belong to Invenia and are not forks and are not archived
invenia_repos = [r for r in repos if r.owner.login == "invenia" and not r.fork and not r.archived]

for repo in repos:
    workflows = repo.get_workflows()

    for workflow in workflows:
        enable_url = workflow.url + "/enable"
        requests.put(enable_url, auth=(name, pat))
