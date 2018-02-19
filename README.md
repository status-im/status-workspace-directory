## Slack Work Directory

Slack Work Directory (SWD) - is a scheduled script that pulls useful information from Github, Geekbot and the BambooHR APIs.
By setting the following fields in an employee's Bamboo HR profile:

_Skype_ field to the employee's slack username.
_Facebook_ field to the employee's github username.
_Twitter Feed_ field to the employee's Status Public Key (retrieved from Status App Profile page)

The Slack Work Directory script can automatically set some extra info fields for the employee's Slack profile fields (https://get.slack.help/hc/en-us/articles/212281478-Customize-member-profiles).

## BambooHR

Job title, phone number, hire date, manager and status public key (Twitter Feed) are retrieved from BambooHR and set on slack.

## Github Ideas

By assigning yourself to an idea at https://github.com/status-im/ideas/issues,
SWD will automatically display you are working on the idea in the 'Working on Ideas' field.

##  Daily standups

Daily status standups get pulled from the geekbot API, only the latest Daily Standup will show.
This is set in the "Latest standup" field on slack.

## Required Environment Variables

BAMBOO_HR_TOKEN
SLACK_BOT_TOKEN
SLACK_API_TOKEN
GEEKBOT_API_TOKEN
