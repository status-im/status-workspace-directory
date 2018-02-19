#!/usr/bin/env python3

import time

from slack_members import map_member_ids, set_profile, get_profile
from bamboo_employees import get_employees, get_employee
from github import get_issues_assigned_to
from geekbot_standups import get_latest_standup

_, employees_name_map = get_employees()
slack_profile_map = map_member_ids()


# Map for looking up slack profiles for a given bamboo id.
bamboo_id_slack_user_map = {
    employees_name_map[slack_name]["id"]: slack_user
    for slack_name, slack_user in slack_profile_map.items() if employees_name_map.get(slack_name)
}


def gh_username(instr):
    if not instr:
        return None
    if instr.startswith("http") or "/" in instr:
        return instr.split("/")[-1]
    return instr


def add_trailing_slash(instr, length=245):
    if len(instr) >= length:
        return instr[:length] + '...'


def final_set():
    for slack_name, slack_user in slack_profile_map.items():
        bamboo_details = employees_name_map.get(slack_name)

        if not bamboo_details:
            continue

        try:
            github_username = gh_username(bamboo_details["facebook"])

            # Get assigned issues
            assigned_issues = []
            if github_username:
                assigned_issues = get_issues_assigned_to(github_username)

            # Get supervisor
            bamboo_extra_details = get_employee(bamboo_details["id"])
            slack_supervisor_id = bamboo_id_slack_user_map.get(bamboo_extra_details["supervisorEId"], {}).get("id", "")

            # Get last standup
            standup = get_latest_standup(slack_user["id"])
            standup_str = ""
            if standup:
                sarr = []
                for question in standup["questions"]:
                    # sarr.append(question["question"])
                    sarr.append(question["answer"].replace('<br />', ';'))
                standup_str = " ".join(sarr)

            payload = {
                "title": bamboo_details["jobTitle"],
                "phone": bamboo_details["mobilePhone"],
                "fields": {
                    "Xf8LSC9MEC": {  # Start Date
                        "value": bamboo_extra_details["hireDate"],
                        "alt": ""
                    },
                    "Xf8ME3KUM9": {  # Github
                        "value": github_username,
                        "alt": ""
                    },
                    "Xf8NC9BLBG": {  # Manager
                        "value": slack_supervisor_id or "",
                        "alt": ""
                    },
                    "Xf8QLU2BPA": {  # Current Ideas
                        "value": ",".join([issue["title"] + " " + issue["url"] for issue in assigned_issues]),
                        "alt": ""
                    },
                    "Xf8QPT2ECR": {  # Latest standup
                        "value": add_trailing_slash(standup_str),
                        "alt": ""
                    }
                }
            }

            res = set_profile(slack_user["id"], payload)
        except Exception as e:
            print(e)
            res = {'ok': False}

        if not res['ok']:
            print('Failed to set: ' + slack_name)
        else:
            print('Profile set: ', slack_name)


if __name__ == '__main__':
    while True:
        final_set()
        print('Sleeping for 1h')
        time.sleep(3600)
