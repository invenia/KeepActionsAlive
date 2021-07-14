# KeepActionsAlive
Prevent scheduled GitHub Actions from becoming disabled after 60 days

## How to use

This requires installing the github api package, which can be done with `python -m pip install github`

Afterwards this can be started by setting the following environment variables:
* `GH_USER`
  * Your Github username
  * Used for authenticating the API call to re-enable workflows
* `GH_LOGIN_OR_TOKEN`
  * Used both for API calls to get repo/organization info, and to send the request to re-enable workflows
  * A Github [Personal Access Token (PAT)](https://docs.github.com/en/rest/overview/other-authentication-methods#via-oauth-and-personal-access-tokens)
* `GH_ORGANIZATION`
  * The name of the organization you would like to work with
  * Used to fetch the list of all owned repositories, and then all workflows
  * The user specified by `GH_USER` will need permission to re-enable workflows in this organization with the token specified by `GH_LOGIN_OR_TOKEN`
