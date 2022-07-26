from discord.ext import commands
from typing import Optional
from lib.consts import CONSTS
from lib.misc import guild
from discord.utils import MISSING
from discord import app_commands
import discord
from lib.voting.actions.action import Action

class CreateTextChannelAction(Action):
    ID = 0

    def __init__(self, name, category_id, position, desc):
        super().__init__(name=name, category_id=category_id, position=position, desc=desc)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        if self.category_id != None:
            ct = await gu.fetch_channel(self.category_id)
        else:
            ct = None
        await gu.create_text_channel(self.name, position=self.position if self.position!=None else MISSING, category=ct, topic=self.desc if self.desc!=None else MISSING)

    def message(self):
        return f'Proposal to create a text channel called { self.name }.'

class DeleteChannelAction(Action):
    ID = 1

    def __init__(self, channel_id):
        super().__init__(channel_id=channel_id)
    
    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        ct = await gu.fetch_channel(self.channel_id)
        await ct.delete()
    
    def message(self):
        return f'Proposal to delete a text channel'

def register_channel_actions(bot: commands.Bot, f):
    channel_g = app_commands.Group(name="channel", description="actions related to channels")
    create_g = app_commands.Group(name="create", description="create a channel", parent=channel_g)
    delete_g = app_commands.Group(name="delete", description="delete a channel", parent=channel_g)

    @create_g.command(name="text")
    @app_commands.describe(name="The name of the channel you want to create", category="The category you want to add the channel to",)
    async def create_text_channel(interaction: discord.Interaction, name: str, category: Optional[discord.CategoryChannel], position: Optional[int], desc: Optional[str]):
        await f(bot, interaction, 0, name=name, category_id=category.id if category != None else None, position=position, desc=desc)
    
    @delete_g.command(name="nonthread")
    @app_commands.describe(channel="The channel to delete")
    async def delete_channel(interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        if channel.id in CONSTS.notouch:
            await interaction.response.send_message(f'You cannot delete <#{ channel.id }>.', ephemeral=True)
        else:
            await f(bot, interaction, 1, channel_id=channel.id)
    
    @delete_g.command(name="thread")
    @app_commands.describe(thread="The thread to delete")
    async def delete_thread(interaction: discord.Interaction, thread: discord.Thread):
        await f(bot, interaction, 1, channel_id=thread.id)

    bot.tree.add_command(channel_g)