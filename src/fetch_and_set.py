#!/usr/bin/env python3
import json
import time

from pathlib import Path
from slack_members import map_member_ids, set_profile, get_profile
from bamboo_employees import get_employees, get_employee
from github import get_issues_assigned_to, upload_contacts_to_gist
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


def write_out_public_keys(public_keys):

    existing_contacts = {}
    if Path('contacts.json').exists():
        with open('contacts.json', 'r') as f:
            existing_contacts = json.load(f)

    updated_contacts = False
    for k in public_keys.keys():
        if k not in existing_contacts:
            updated_contacts = True
            break

    if updated_contacts:
        print('New public key(s) found writing contacts.json')
        with open('contacts.json', 'w') as f:
            json.dump(public_keys, f)
        if upload_contacts_to_gist('contacts.json'):
            print('Uploaded gist successfully')
        else:
            print('Failed to upload gist')

def final_set():
    # Create json contact file.
    public_keys = {}
    for _, bamboo_details in employees_name_map.items():
        pub_key = bamboo_details["twitterFeed"]
        if pub_key and pub_key.startswith('0x'):
            public_keys[pub_key] = {  # kept for json contacts file.
                "name": {
                    "en":  ' '.join([
                        bamboo_details.get('firstName', ''),
                        bamboo_details.get('lastName', '')])
                },
                "photo-path": bamboo_details.get('photoUrl', ''),
                "add-chat?": False,
                "dapp?": False
            }
    write_out_public_keys(public_keys)

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
                    },
                }
            }

            if bamboo_details["twitterFeed"]:
                pub_key = bamboo_details["twitterFeed"]
                payload["fields"]["Xf8MDHK94H"] = {  # Set Status Public Key
                    "value": pub_key,
                    "alt": ""
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
