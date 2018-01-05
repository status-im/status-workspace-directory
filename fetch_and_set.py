from slack_members import map_member_ids, set_profile
from bamboo_employees import get_employees


_, employees_name_map = get_employees()
slack_profile_map = map_member_ids()

# import ipdb; ipdb.set_trace()

for slack_name, slack_user in slack_profile_map.items():
    bamboo_details = employees_name_map.get(slack_name)

    if slack_name == 'jacqueswww':
        print('found one:')
        print(slack_user)
        print(bamboo_details)

        payload = {
            "user": slack_user["id"]
        }
        set_profile('users.profile.set', payload)
        break
