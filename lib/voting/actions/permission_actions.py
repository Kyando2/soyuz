from typing import Optional
from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
from discord import app_commands
import discord
from lib.voting.actions.action import Action
from lib.voting.system import ACTION_DICT

@ACTION_DICT.register()
class PermsChannelBlockRole(Action):
    ID = 16

    def __init__(self, role_id, channel_id):
        super().__init__(role_id=role_id, channel_id=channel_id)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        ch = await gu.fetch_channel(self.channel_id)
        r = gu.get_role(self.role_id)
        await ch.edit(overwrites={r: discord.PermissionOverwrite(send_messages=False)})

    def message(self):
        return f'Proposition to block role <@&{ self.role_id }> from typing in channel <#{ self.channel_id }>'

def register_permission_actions(bot: commands.Bot, f):
    perms_g = app_commands.Group(name="perms", description="actions related to perms")
    channel_g = app_commands.Group(name="channel", description="actions related to channel permissions", parent=perms_g)
    
    @channel_g.command(name="block_role", description="Blocks a role from seeing a channel")
    @app_commands.describe(role="The role to block from talking in this channel", channel="The channel to block the role from talking in")
    async def perms_channel_role_block(interaction: discord.Interaction, role: discord.Role, channel: discord.abc.GuildChannel):
        await f(bot, interaction, 16, role_id=role.id, channel_id=channel.id)

    bot.tree.add_command(perms_g)