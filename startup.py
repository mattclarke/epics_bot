
import os



BOT_ID = '
BOT_CHANNEL_ID = ''
SLACK_BOT_TOKEN = ''

# Need to tell PyEpics where the ca library is
os.environ["PYEPICS_LIBCA"] = "/opt/epics/bases/base-3.15.5/lib/linux-x86_64/libca.so"

if __name__ == '__main__':
    from epicsbot import EpicsBot
    bot = EpicsBot(BOT_ID, BOT_CHANNEL_ID, SLACK_BOT_TOKEN)
    bot.start_bot()
