from typing import Optional
from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
from discord import app_commands
import discord
from lib.voting.actions.action import Action
from lib.voting.system import ACTION_DICT

@ACTION_DICT.register()
class SomeAction(Action):
    ID = -1

    def __init__(self, a, b, c):
        super().__init__(a=a, b=b, c=c,)

    async def run(self, bot: commands.Bot):
        pass # do stuff

    def message(self):
        return f'My cool message!'

def register_template_actions(bot: commands.Bot, f):
    template_g = app_commands.Group(name="template", description="template you should not see this")

    @template_g.command(name="edit")
    @app_commands.describe(role="The role to edit", name="The new name for the role", r="Red", g="Green", b="Blue")
    async def template(interaction: discord.Interaction, role: discord.Role, a: int, b: int, c: int):
        await f(bot, interaction, -1, a=a, b=b, c=c)

    bot.tree.add_command(template)