from typing import Optional
from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
from discord import app_commands
import discord
from lib.voting.actions.action import Action
from lib.voting.system import ACTION_DICT

def register_emoji_actions(bot: commands.Bot, f):
    emoji_g = app_commands.Group(name="emoji", description="actions related to emojis and stickers")

    #bot.tree.add_command(emoji_g)