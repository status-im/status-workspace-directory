from slack_members import map_member_ids, set_profile, get_profile
from bamboo_employees import get_employees
from github import get_issues_assigned_to

_, employees_name_map = get_employees()
slack_profile_map = map_member_ids()


def gh_username(instr):
    if instr.startswith("http"):
        return instr.split("/")[-1]
    return instr


for slack_name, slack_user in slack_profile_map.items():
    bamboo_details = employees_name_map.get(slack_name)

    if slack_name == 'cryptowanderer':
        github_username = gh_username(bamboo_details["facebook"])
        payload = {
            "title": bamboo_details["jobTitle"],
            "phone": bamboo_details["mobilePhone"],
            "fields": {
                # "Xf8MDHK94H": {  # Status public key
                #     "value": "test_public_keyyyy",
                #     "alt": ""
                # },
                "Xf8LSC9MEC": {  # Start Date
                    "value": "1970-01-01",
                    "alt": ""
                },
                "Xf8ME3KUM9": {  # Github
                    "value": github_username,
                    "alt": ""
                }
            }
        }

        print('%s issues: ' % github_username)
        assigned_issues = get_issues_assigned_to(github_username)
        for issue in assigned_issues:
            print(issue)

        print('payload:')
        print(payload)

        res = set_profile(slack_user["id"], payload)

        print('set_profile:')
        print(res)

        if not res['ok']:
            print('Failed to set: ' + slack_name)

        break
