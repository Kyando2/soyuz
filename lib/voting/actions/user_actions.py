from datetime import timedelta
from typing import Optional
from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
from discord import app_commands
import discord
from lib.voting.actions.action import Action

class UserAddRoleAction(Action):
    ID = 7

    def __init__(self, user_id, role_id):
        super().__init__(user_id=user_id, role_id=role_id)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        u = await gu.fetch_member(self.user_id)
        await u.add_roles(discord.Object(self.role_id))

    def message(self):
        return f'Proposal to add role <@&{ self.role_id }> to user <@{ self.user_id }>.'

class UserModKickAction(Action):
    ID = 8

    def __init__(self, user_id):
        super().__init__(user_id=user_id)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        u = await gu.fetch_member(self.user_id)
        await u.kick()

    def message(self):
        return f'Proposal to kick user <@{ self.user_id }>.'

    
class UserModBanAction(Action):
    ID = 9

    def __init__(self, user_id):
        super().__init__(user_id=user_id)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        u = await gu.fetch_member(self.user_id)
        await u.ban()

    def message(self):
        return f'Proposal to ban user <@{ self.user_id }>.'


class UserModTimeoutAction(Action):
    ID = 10

    def __init__(self, user_id, dt):
        super().__init__(user_id=user_id, dt=dt)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        u = await gu.fetch_member(self.user_id)
        await u.timeout(timedelta(minutes=self.dt))

    def message(self):
        return f'Proposal to timeout user <@{ self.user_id }> for { self.dt } minutes.'

def register_user_actions(bot: commands.Bot, f):
    user_g = app_commands.Group(name="user", description="actions related to users")
    role_g = app_commands.Group(name="role", description="actions related to roles", parent=user_g)
    mod_g = app_commands.Group(name="mod", description="actions related to moderation", parent=user_g)

    @role_g.command(name="add")
    @app_commands.describe(user="The user to give the role to", role="The role to give to that user")
    async def user_add_role(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        await f(bot, interaction, 7, user_id=user.id, role_id=role.id)

    @mod_g.command(name="kick")
    @app_commands.describe(user="The user to kick")
    async def user_mod_kick(interaction: discord.Interaction, user: discord.Member):
        await f(bot, interaction, 8, user_id=user.id)
    
    @mod_g.command(name="ban")
    @app_commands.describe(user="The user to ban")
    async def user_mod_ban(interaction: discord.Interaction, user: discord.Member):
        await f(bot, interaction, 9, user_id=user.id)
    
    @mod_g.command(name="timeout")
    @app_commands.describe(user="The user to timeout", time="The amount of time to timeout")
    async def user_mod_timeout(interaction: discord.Interaction, user: discord.Member, time: int):
        await f(bot, interaction, 10, user_id=user.id, dt=time)

    bot.tree.add_command(user_g)