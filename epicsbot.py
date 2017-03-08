import os
import time
from command_parser import as_string_requested, extract_pv_name, uzhex_requested
from slackclient import SlackClient
from epics_fetcher import EpicsFetcher, PvNotFoundException

BOT_ID = os.environ.get("BOT_ID")
BOT_CHANNEL_ID = os.environ.get("BOT_CHANNEL_ID")
CAGET_COMMAND = "caget "
# Instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


class EpicsBot(object):

    def __init__(self, bot_id=BOT_ID, bot_channel=BOT_CHANNEL_ID):
        """
        The constructor.

        :param bot_id: the unique Slack ID for the bot - don't put this in the code
        :param bot_channel: the unique Slack ID for the bot's channel - don't put this in the code
        """
        self.bot_id = bot_id
        self.bot_channel = bot_channel
        self.at_bot = "<@" + bot_id + ">"

    def parse_caget_command(self, command):
        """
        Parses the caget command and extracts the important information.

        :param command: the command received over Slack
        :return: a tuple containing whether a string was requested, the PV name and whether un-hexing was required
        """
        as_str = as_string_requested(command)
        name = extract_pv_name(command)
        as_uzhex = uzhex_requested(command)
        return as_str, name, as_uzhex

    def handle_command(self, command, channel, epics_fetcher=EpicsFetcher()):
        """
        Receives commands directed at the bot and determines if they
        are valid commands. Depending on the command it will response appropriately.

        :param command: the command
        :param channel: the channel the message was sent on
        """
        response = "I'm sorry Dave I'm afraid I can't do that. Try 'caget'."
        if command.startswith(CAGET_COMMAND):
            try:

                as_str, name, as_uzhex = self.parse_caget_command(command)
                # If as_uzhex specified then we must get it as a string
                ans = epics_fetcher.caget(name, as_str or as_uzhex)
                if as_uzhex:
                    ans = epics_fetcher.dehex_and_decompress(ans)
                # Restrict the message length to less than 500 chars
                if as_str and len(ans) > 500:
                    ans = ans[0:495] + "..."
                response = "```%s```" % ans
            except PvNotFoundException as err:
                response = err.message
            except Exception as err:
                response = "Sorry, something went wrong: %s" % err
                print(response)
        return response

    def send_response(self, channel, response):
        """
        Send the response to Slack.

        :param channel: the channel to sent the response to
        :param response: the response string
        """
        try:
            slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)
        except Exception as err:
            print('Could not send response to Slack: %s' % err)

    def parse_slack_output(self, slack_rtm_output):
        """
        The Slack Real Time Messaging API is an events firehose.
        This parsing function returns None unless a message is
        directed at the bot either by an @epics_bot or via its channel.

        :param slack_rtm_output: the Slack message
        :return: a tuple of the message text and the channel to reply on
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            print(output_list)
            for output in output_list:
                if output and 'text' in output and self.at_bot in output['text']:
                    # The bot is specified by an '@'
                    # extract text after the @ mention, whitespace removed
                    return output['text'].split(self.at_bot)[1].strip(), output['channel']
                elif output and 'text' in output and 'channel' in output and output['channel'] == self.bot_channel:
                    # The message was send to the bot's channel
                    # Check it is not the bot posting to it's own channel otherwise it will get stuck in a loop
                    if output['user'] != self.bot_id:
                        return output['text'].strip(), output['channel']
        return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("EpicsBot connected and running!")
        bot = EpicsBot()
        while True:
            try:
                command, channel = bot.parse_slack_output(slack_client.rtm_read())
                if command and channel:
                    res = bot.handle_command(command, channel)
                    bot.send_response(channel, res)
                time.sleep(READ_WEBSOCKET_DELAY)
            except Exception as err:
                print('There was an unhandled exception: %s' % err)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
