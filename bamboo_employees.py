import os
import sys
import requests


BAMBOO_HR_TOKEN = os.environ.get('BAMBOO_HR_TOKEN')
if not BAMBOO_HR_TOKEN:
    print('Need bamboohr token')
    sys.exit()


def get_employees():
    url = "https://api.bamboohr.com/api/gateway.php/statusim/v1/employees/directory"

    headers = {
        'Accept': "application/json",
        'Authorization': "Basic %s" % BAMBOO_HR_TOKEN,
    }
    resp = requests.request("GET", url, headers=headers)
    print(resp)
    employees = resp.json()["employees"]
    employees_name_map = {emp["skypeUsername"]: emp for emp in employees}

    return employees, employees_name_map
