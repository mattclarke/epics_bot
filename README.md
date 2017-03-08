# epics_bot
The Slackbot for talking EPICS

## How run it

Set environment variables for:

* "BOT_ID"
* "BOT_CHANNEL_ID"
* "SLACK_BOT_TOKEN"

These values can be obtain from Slack. The "SLACK_BOT_TOKEN" will be assign when you create the bot via Slack's webpage.

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
