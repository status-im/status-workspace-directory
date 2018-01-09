import requests


def get_issues_assigned_to(username):
    # /repos/:owner/:repo/issues

    url = "https://api.github.com/repos/status-im/ideas/issues"
    params = {'assignee': username, 'state': 'open'}
    resp = requests.get(url, params=params)

    return resp.json()
