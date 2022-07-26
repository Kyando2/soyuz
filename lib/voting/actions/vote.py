from discord.ext import commands
from lib.voting.actions.channel_actions import register_channel_actions
from lib.voting.actions.message_actions import register_message_actions

def register_actions(bot: commands.Bot, f):
    register_channel_actions(bot, f)
    register_message_actions(bot, f)
