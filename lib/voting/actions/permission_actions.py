from typing import Optional
from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
from discord import app_commands
import discord
from lib.voting.actions.action import Action
from lib.voting.system import ACTION_DICT

def register_permission_actions(bot: commands.Bot, f):
    perms_g = app_commands.Group(name="perms", description="actions related to perms")

    #bot.tree.add_command(perms_g)