import os
import requests


BAMBOO_HR_TOKEN = os.environ.get('BAMBOO_HR_TOKEN')


def get_employees():
    url = "https://api.bamboohr.com/api/gateway.php/statusim/v1/employees/directory"

    headers = {
        'Accept': "application/json",
        'Authorization': "Basic %s" % BAMBOO_HR_TOKEN,
    }
    resp = requests.request("GET", url, headers=headers)

    employees = resp.json()["employees"]
    employees_name_map = {emp["skypeUsername"]: emp for emp in employees}

    return employees, employees_name_map
