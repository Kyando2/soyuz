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
    template_g = app_commands.Group(name="template", description="template")

    @template_g.command(name="template")
    @app_commands.describe(a="template", b="template", c="template")
    async def template(interaction: discord.Interaction, a: int, b: int, c: int):
        await f(bot, interaction, -1, a=a, b=b, c=c)

    bot.tree.add_command(template)