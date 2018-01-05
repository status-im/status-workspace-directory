import os

from slackclient import SlackClient


slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)


def map_member_ids():
    res = sc.api_call("users.list")
    return {
        member['name']: member
        for member in res['members']
    }


def set_profile(data):
    return sc.api_call("users.profile.set", **data)
