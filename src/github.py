import os
import requests

GIST_API_USER = os.environ.get('GIST_API_USER')
GIST_API_KEY = os.environ.get('GIST_API_KEY')
GIST_ID = os.environ.get('GIST_ID')


def get_issues_assigned_to(username):
    # /repos/:owner/:repo/issues

    url = "https://api.github.com/repos/status-im/ideas/issues"
    params = {'assignee': username, 'state': 'open'}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        return []


def upload_contacts_to_gist(file_path):
    url = "https://api.github.com/gists/%s" % GIST_ID

    with open(file_path, 'r') as f:
        content = f.read()
        params = {
            "description": "the description for this gist",
            "files": {
                "contacts.json": {
                    'content': content
                }
            }
        }

        resp = requests.patch(
            url,
            auth=(GIST_API_USER, GIST_API_KEY),
            json=params
        )

        if resp.status_code == 200:
            return True
        else:
            return False
