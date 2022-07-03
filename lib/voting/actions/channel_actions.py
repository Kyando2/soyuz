from discord.ext import commands
from typing import Optional
from lib.consts import CONSTS
from lib.misc import guild, channel
from discord.utils import MISSING
from discord import app_commands
import discord
from lib.voting.actions.action import Action
class CreateTextChannelAction(Action):
    def __init__(self, name, category_id, position):
        super().__init__(name=name, category_id=category_id, position=position)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        if self.category_id != None:
            ct = await gu.fetch_channel(self.category_id)
        else:
            ct = None
        await gu.create_text_channel(self.name, position=self.position if self.position!=None else MISSING, category=ct)

    def ID(self):
        return 0

    def as_dict(self):
        return {
            "name": self.name,
            "category_id": self.category_id,
            "position": self.position
        }
    
    def message(self):
        return f'Proposal to create a text channel called { self.name }.'

def register_channel_actions(bot: commands.Bot, f):
    @bot.tree.command()
    @app_commands.describe(name="The name of the channel you want to create", category="The category you want to add the channel to",)
    async def create_text_channel(interaction: discord.Interaction, name: str, category: Optional[discord.CategoryChannel], position: Optional[int]):
        await f(bot, interaction, 0, name=name, category_id=category.id if category != None else None, position=position)