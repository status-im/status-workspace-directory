import os
import requests
import datetime


GEEKBOT_API_TOKEN = os.environ.get('GEEKBOT_API_TOKEN')


headers = {
    'Authorization': GEEKBOT_API_TOKEN
}


def list_standups():
    url = "https://api.geekbot.io/v1/standups/"
    resp = requests.get(url, headers=headers)
    return resp.json()


def get_latest_standup(user_id, standup_id=12889):
    url = "https://api.geekbot.io/v1/reports/"
    params = {
        "standup_id": standup_id,
        "user_id": user_id,
        "after": (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
    }
    resp = requests.get(url, params=params, headers=headers)

    if resp.status_code != 200:
        return None

    standups = resp.json()

    if standups:
        return standups[0]
    else:
        return None
