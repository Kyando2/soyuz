from discord.ext import commands
from lib.voting.actions.channel_actions import register_channel_actions
from lib.voting.actions.emoji_actions import register_emoji_actions
from lib.voting.actions.message_actions import register_message_actions
from lib.voting.actions.permission_actions import register_permission_actions
from lib.voting.actions.role_actions import register_role_actions
from lib.voting.actions.setting_actions import register_settings_actions
from lib.voting.actions.user_actions import register_user_actions

def register_actions(bot: commands.Bot, f):
    register_channel_actions(bot, f)
    register_message_actions(bot, f)
    register_role_actions(bot, f)
    register_user_actions(bot, f)
    register_permission_actions(bot, f)
    register_settings_actions(bot, f)
    register_emoji_actions(bot, f)