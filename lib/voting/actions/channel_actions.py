from discord.ext import commands
from typing import Optional
from lib.consts import CONSTS
from lib.misc import guild
from discord.utils import MISSING
from discord import app_commands
import discord
from lib.voting.actions.action import Action
from lib.voting.system import ACTION_DICT
@ACTION_DICT.register()
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

@ACTION_DICT.register()
class CreateVoiceChannelAction(Action):
    ID = 12

    def __init__(self, name, category_id, position):
        super().__init__(name=name, category_id=category_id, position=position)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        if self.category_id != None:
            ct = await gu.fetch_channel(self.category_id)
        else:
            ct = None
        await gu.create_voice_channel(self.name, position=self.position if self.position!=None else MISSING, category=ct)

    def message(self):
        return f'Proposal to create a voice channel called { self.name }.'

@ACTION_DICT.register()
class CreateCategoryChannelAction(Action):
    ID = 13

    def __init__(self, name, position):
        super().__init__(name=name, position=position)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        t = await gu.create_category(self.name, position=self.position if self.position!=None else MISSING)
        print(type(t))

    def message(self):
        return f'Proposal to create a category channel called { self.name }.'

@ACTION_DICT.register()
class MoveChannelAction(Action):
    ID = 14

    def __init__(self, channel_id, category_id):
        super().__init__(channel_id=channel_id, category_id=category_id)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        ct = await gu.fetch_channel(self.category_id)
        ch = await gu.fetch_channel(self.channel_id)
        await ch.edit(category=ct)

    def message(self):
        return f'Proposal to move channel <#{ self.channel_id }> to category <#{ self.category_id }>.'

@ACTION_DICT.register()
class DeleteChannelAction(Action):
    ID = 1

    def __init__(self, channel_id):
        super().__init__(channel_id=channel_id)
    
    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        ct = await gu.fetch_channel(self.channel_id)
        await ct.delete()
    
    def message(self):
        return f'Proposal to delete <#{ self.channel_id }>'

@ACTION_DICT.register()
class PurgeChannelAction(Action):
    ID = 4

    def __init__(self, channel_id, num):
        super().__init__(channel_id=channel_id, num=num)
    
    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        ct = await gu.fetch_channel(self.channel_id)
        await ct.purge(limit=self.num)
    
    def message(self):
        return f'Proposal to purge the channel <#{ self.channel_id }>'


def register_channel_actions(bot: commands.Bot, f):
    channel_g = app_commands.Group(name="channel", description="actions related to channels")
    create_g = app_commands.Group(name="create", description="create a channel", parent=channel_g)
    delete_g = app_commands.Group(name="delete", description="delete a channel", parent=channel_g)

    @create_g.command(name="text")
    @app_commands.describe(name="The name of the channel you want to create", category="The category you want to add the channel to", position="The position of the channel", desc="The description of the channel")
    async def create_text_channel(interaction: discord.Interaction, name: str, category: Optional[discord.CategoryChannel], position: Optional[int], desc: Optional[str]):
        await f(bot, interaction, 0, name=name, category_id=category.id if category != None else None, position=position, desc=desc)

    @create_g.command(name="voice")
    @app_commands.describe(name="The name of the channel you want to create", category="The category you want to add the channel to", position="The position of the channel")
    async def create_voice_channel(interaction: discord.Interaction, name: str, category: Optional[discord.CategoryChannel], position: Optional[int]):
        await f(bot, interaction, 12, name=name, category_id=category.id if category != None else None, position=position)

    @create_g.command(name="category")
    @app_commands.describe(name="The name of the channel you want to create", position="The position of the channel")
    async def create_category_channel(interaction: discord.Interaction, name: str, position: Optional[int]):
        await f(bot, interaction, 13, name=name, position=position)
    
    @delete_g.command(name="nonthread")
    @app_commands.describe(channel="The channel to delete")
    async def delete_channel(interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        if channel.id in CONSTS.notouch:
            await interaction.response.send_message(f'You cannot delete <#{ channel.id }>.', ephemeral=True)
        else:
            await f(bot, interaction, 1, channel_id=channel.id)

    @channel_g.command(name="move")
    @app_commands.describe(channel="The channel to move", category="The category to move it to")
    async def move_channel(interaction: discord.Interaction, channel: discord.abc.GuildChannel, category: discord.CategoryChannel):
        if channel.id in CONSTS.notouch:
            await interaction.response.send_message(f'You cannot move <#{ channel.id }>.', ephemeral=True)
        else:
            await f(bot, interaction, 14, channel_id=channel.id, category_id=category.id)
    
    @delete_g.command(name="thread")
    @app_commands.describe(thread="The thread to delete")
    async def delete_thread(interaction: discord.Interaction, thread: discord.Thread):
        await f(bot, interaction, 1, channel_id=thread.id)

    @channel_g.command(name="purge")
    @app_commands.describe(channel="The channel to purge", num="The amount of messages to purge")
    async def channel_purge(interaction: discord.Interaction, channel: discord.TextChannel, num: int):
        await f(bot, interaction, 4, channel_id=channel.id, num=num)

    bot.tree.add_command(channel_g)