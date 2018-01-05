import requests
import os
import json

from slackclient import SlackClient


slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)


def map_member_ids():
    res = sc.api_call("users.list")
    return {
        member['name']: member
        for member in res['members']
    }


def get_profile(user_id):
    return sc.api_call("users.profile.get", include_labels=True, user=user_id)


def set_profile(user_id, data):

    headers = {
        "Authorization": "Bearer " + slack_token
    }
    url = "https://slack.com/api/users.profile.set"
    data_str = json.dumps(data)
    params = {
        'user': user_id,
        'profile': data_str
    }
    resp = requests.post(url, headers=headers, params=params)

    return resp.json()
