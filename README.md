# epics_bot
The Slackbot for talking EPICS.

## How to run it

Find your values for the following and put them in the appropriate place in startup.py

* BOT_ID
* BOT_CHANNEL_ID
* SLACK_BOT_TOKEN

These values can be obtain from Slack. The "SLACK_BOT_TOKEN" will be assigned when you create the bot via your team's Slack webpage.

The other details can be obtained via code, for example the "BOT_ID" can be found like so:

```python
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

api_call = slack_client.api_call("users.list")
if api_call.get('ok'):
    # Get the users
    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == "MY_BOTS_NAME":
            print user.get('id')
```

WARNING: keep your values safe, do not check them into git or display them on a public website.

To run the bot type:
```
python startup.py
```
