import unittest
import mock
from epics_fetcher import EpicsFetcher
from epicsbot import EpicsBot

BOT_ID = u'MYBOTID'
BOT_CHANNEL = u'BOTCHANNEL'
NON_BOT_CHANNEL = u'SOMECHANNEL'


class TestEpicsBot(unittest.TestCase):
    def setUp(self):
        self.bot_id = BOT_ID
        self.bot_channel = BOT_CHANNEL
        self.bot = EpicsBot(self.bot_id, self.bot_channel)
        self.msg_to_bot_channel = [
            {u'text': u'caget IN:DEMO:SIMPLE:VALUE1', u'ts': u'1488965605.000074',
             u'user': u'AAAAAAAAA', u'team': u'AAAAAAAAA', u'type': u'message', u'channel': BOT_CHANNEL}]
        self.str_msg_to_bot_channel = [
            {u'text': u'caget -S IN:DEMO:SIMPLE:VALUE1', u'ts': u'1488965605.000074',
             u'user': u'AAAAAAAAA', u'team': u'AAAAAAAAA', u'type': u'message', u'channel': BOT_CHANNEL}]
        self.uzhex_msg_to_bot_channel = [
            {u'text': u'caget -S IN:DEMO:CS:BLOCKSERVER:BLOCKNAMES | uzhex', u'ts': u'1488965605.000074',
             u'user': u'AAAAAAAAA', u'team': u'AAAAAAAAA', u'type': u'message', u'channel': BOT_CHANNEL}]
        self.msg_at_bot = [
            {u'text': u'<@' + self.bot_id + u'> caget IN:DEMO:SIMPLE:VALUE1', u'ts': u'1488965605.000074',
             u'user': u'AAAAAAAAA', u'team': u'AAAAAAAAA', u'type': u'message', u'channel': NON_BOT_CHANNEL}]
        self.msg_not_to_bot = [
            {u'text': u'Hello', u'ts': u'1488965605.000074',
             u'user': u'AAAAAAAAA', u'team': u'AAAAAAAAA', u'type': u'message', u'channel': NON_BOT_CHANNEL}]

    def test_parsing_slack_output_finds_when_channel_is_bot_channel(self):
        cmd, chan = self.bot.parse_slack_output(self.uzhex_msg_to_bot_channel)

        self.assertEqual(self.bot_channel, chan)

    def test_parsing_slack_output_returns_none_when_nothing_to_do_with_bot(self):
        cmd, chan = self.bot.parse_slack_output(self.msg_not_to_bot)

        self.assertEqual(None, cmd)
        self.assertEqual(None, chan)

    def test_parsing_slack_output_finds_correct_channel_when_at_bot_on_any_channel(self):
        cmd, chan = self.bot.parse_slack_output(self.msg_at_bot)

        self.assertEqual(u'SOMECHANNEL', chan)

    def test_handle_command_handles_caget_exception(self):
        cmd, chan = self.bot.parse_slack_output(self.msg_at_bot)

        fetcher = EpicsFetcher()
        fetcher.caget = mock.MagicMock(side_effect=Exception('Boom!'))

        # This should not raise an exception
        self.bot.handle_command(cmd, chan, fetcher)

    def test_handle_command_handles_caget_float(self):
        cmd, chan = self.bot.parse_slack_output(self.msg_at_bot)
        value = 2.0

        fetcher = EpicsFetcher()
        fetcher.caget = mock.MagicMock()
        fetcher.caget.return_value = value

        self.assertEqual("```%s```" % value, self.bot.handle_command(cmd, chan, fetcher))

    def test_handle_command_handles_caget_float_as_str(self):
        cmd, chan = self.bot.parse_slack_output(self.str_msg_to_bot_channel)

        fetcher = EpicsFetcher()
        fetcher.caget = mock.MagicMock()
        fetcher.caget.return_value = "2"

        self.assertEqual("```2```", self.bot.handle_command(cmd, chan, fetcher))


if __name__ == '__main__':
    unittest.main()
