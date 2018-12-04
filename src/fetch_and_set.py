#!/usr/bin/env python3
import json
import time

from datetime import datetime
from pathlib import Path
from bamboo_employees import get_employees
from github import upload_contacts_to_gist


def gh_username(instr):
    if not instr:
        return None
    if instr.startswith("http") or "/" in instr:
        return instr.split("/")[-1]
    return instr


def write_out_public_keys(public_keys):

    existing_contacts = {}
    contacts_path = '/tmp/contacts.json'
    if Path(contacts_path).exists():
        with open(contacts_path, 'r') as f:
            existing_contacts = json.load(f)

    updated_contacts = False
    for k in public_keys.keys():
        if k not in existing_contacts:
            updated_contacts = True
            break

    if updated_contacts:
        print('New public key(s) found writing contacts.json')
        with open(contacts_path, 'w') as f:
            json.dump(public_keys, f)
        if upload_contacts_to_gist(contacts_path):
            print(datetime.now().isoformat(), 'Uploaded gist successfully')
        else:
            print(datetime.now().isoformat(), 'Failed to upload gist')
    else:
        print(datetime.now().isoformat(), 'Nothing new to upload.')


def final_set():
    # Fetch from bamboo
    employees_list, employees_name_map = get_employees()

    # Create json contact file.
    public_keys = {}
    for bamboo_details in employees_list:
        pub_key = bamboo_details["customStatusPublicKey"]
        if pub_key:
            name = bamboo_details['preferredName'] if bamboo_details['preferredName'] else bamboo_details['firstName']
            public_keys[pub_key] = {  # kept for json contacts file.
                "name": {
                    "en": name
                },
                "department": bamboo_details['department'],
                "photo-path": bamboo_details.get('photoUrl', ''),
                "add-chat?": False,
                "dapp?": False
            }
    write_out_public_keys(public_keys)


if __name__ == '__main__':
    while True:
        final_set()
        print('Sleeping for 1h')
        time.sleep(3600)
