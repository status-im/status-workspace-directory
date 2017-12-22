import os
import redis
import json
import requests

from flask import request, abort
from flask import Flask


BAMBOO_HR_TOKEN = os.environ.get('BAMBOO_HR_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
r_handler = redis.StrictRedis(host='localhost', port=6379, db=0)
r_postfix = 'swd'
app = Flask(__name__)


def rget(key, default=None):
    val = r_handler.get(r_postfix + ":" + key)
    if val:
        return json.loads(val.decode())
    return default


def rset(key, val):
    r_handler.set(r_postfix + ":" + key, json.dumps(val))


def populate_employees():
    print('Populating employees')
    url = "https://api.bamboohr.com/api/gateway.php/statusim/v1/employees/directory"

    headers = {
        'Accept': "application/json",
        'Authorization': "Basic %s" % BAMBOO_HR_TOKEN,
    }
    resp = requests.request("GET", url, headers=headers)

    employees = resp.json()["employees"]
    employees_name_map = {emp["skypeUsername"]: emp for emp in employees}

    rset('employees', employees)
    rset('employees_name_map', employees_name_map)


populate_employees()


@app.route('/', methods=['POST'])
def slash_command():
    token = request.form.get('token', None)
    text = request.form.get('text', None)

    if text.startswith('@'):
        text = text[1:]

    if token != SLACK_BOT_TOKEN:
        abort(400)

    employees_name_map = rget('employees_name_map')
    if text not in employees_name_map:
        return "{} not found.".format(text)
    emp = employees_name_map[text]

    profile_txt = """
*Employee #*: {}
*Name*: {}
*Job Title*: {}
*Department*: {}
*Location*: {}
*GH*: {}
    """.format(
        emp["id"],
        emp["displayName"],
        emp["jobTitle"],
        emp["department"],
        emp["location"],
        emp["facebook"]
    )

    return profile_txt
