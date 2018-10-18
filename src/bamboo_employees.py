import os
import sys
import requests


BAMBOO_HR_TOKEN = os.environ.get('BAMBOO_HR_TOKEN')
if not BAMBOO_HR_TOKEN:
    print('Need bamboohr token')
    sys.exit()

headers = {
    'Accept': "application/json",
    'Authorization': "Basic %s" % BAMBOO_HR_TOKEN,
}


def get_employees():
    url = "https://api.bamboohr.com/api/gateway.php/statusim/v1/employees/directory"

    resp = requests.get(url, headers=headers)

    employees = resp.json()["employees"]
    employees_name_map = {}
    employees_list = []
    for emp in employees:
        emp_data = get_employee(emp['id'])
        emp.update(emp_data)
        employees_list.append(emp)
        if emp_data['customSlackusername']:
            employees_name_map[emp_data['customSlackusername']] = emp

    return employees_list, employees_name_map


def get_employee(employee_id):

    url = "https://api.bamboohr.com/api/gateway.php/statusim/v1/employees/{}".format(
        employee_id
    )

    params = {
        'fields': ','.join((
            'supervisor', 'supervisorId', 'supervisorEId',
            'hireDate', 'customGitHubusername', 'customStatusPublicKey',
            'customSlackusername'
        ))
    }
    resp = requests.get(url, params=params, headers=headers)

    return resp.json()
