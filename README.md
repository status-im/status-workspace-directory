## Slack Work Directory

Slack Work Directory (SWD) - is a scheduled script that pulls useful information from Github, Geekbot and the BambooHR APIs.

The Slack Work Directory script can automatically set some extra info fields for the employee's Slack profile fields (https://get.slack.help/hc/en-us/articles/212281478-Customize-member-profiles).

## BambooHR

Job title, phone number, hire date, manager and status public key are retrieved from BambooHR and set on slack.

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

## Run in docker

To run the basic fetch-and-set script in docker:

```
docker build -t swd ./
docker run --env-file env.list swd
```
