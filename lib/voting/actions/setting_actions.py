from typing import Optional
from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
from discord import app_commands
import discord
from lib.voting.actions.action import Action
from lib.voting.system import ACTION_DICT

def register_settings_actions(bot: commands.Bot, f):
    settings_g = app_commands.Group(name="settings", description="actions related to overall server settings")

    #bot.tree.add_command(settings_g)