from bamboo_employees import get_employees
employees, _ = get_employees()

print('Missing github names, set as Facebook field in Bamboo HR:')


for emp in employees:
    if not emp.get('facebook', False):
        print(emp['displayName'])

print('Missing slack names, set as  Skype field in Bamboo HR:')

for emp in employees:
    if not emp.get('skypeUsername', False):
        print(emp['displayName'])
