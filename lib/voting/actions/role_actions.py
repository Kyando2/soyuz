from typing import Optional
from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
from discord import app_commands
import discord
from lib.voting.actions.action import Action
from lib.voting.system import ACTION_DICT

@ACTION_DICT.register()
class CreateRoleAction(Action):
    ID = 5

    def __init__(self, name, color, show, position):
        super().__init__(name=name, color=color, show=show, position=position)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        r = await gu.create_role(name=self.name, color=self.color, hoist=self.show if self.show != None else False)
        if self.position != None:
            rs = await gu.fetch_roles()
            l = len(rs)
            await r.edit(position=l-self.position)

    def message(self):
        return f'Proposal to create a role called { self.name }.'

@ACTION_DICT.register()
class DeleteRoleAction(Action):
    ID = 6

    def __init__(self, role_id):
        super().__init__(role_id=role_id)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        r = gu.get_role(self.role_id)
        await r.delete()

    def message(self):
        return f'Proposal to delete role <@&{ self.role_id }>.'

@ACTION_DICT.register()
class EditRoleAction(Action):
    ID = 11

    def __init__(self, role_id, name, color):
        super().__init__(role_id=role_id, name=name, color=color)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        r = gu.get_role(self.role_id)
        await r.edit(name=self.name, color=self.color)

    def message(self):
        return f'Proposal to edit role <@&{ self.role_id }>\nThis will change its name to { self.name } and its color to { self.color }.'

def register_role_actions(bot: commands.Bot, f):
    role_g = app_commands.Group(name="role", description="actions related to roles")

    @role_g.command(name="create")
    @app_commands.describe(name="The name of the role to create", r="Red", g="Green", b="Blue", show="Whether to show it on the side bar", position="Position of the role, with 0 being at the top")
    async def create_role(interaction: discord.Interaction, name: str, r: int, g: int, b: int, show: Optional[bool], position: Optional[int]):
        await f(bot, interaction, 5, name=name, color=discord.Color.from_rgb(r, g, b).value, show=show, position=position)

    @role_g.command(name="delete")
    @app_commands.describe(role="The role to delete")
    async def delete_role(interaction: discord.Interaction, role: discord.Role):
        await f(bot, interaction, 6, role_id=role.id)

    @role_g.command(name="edit")
    @app_commands.describe(role="The role to edit", name="The new name for the role", r="Red", g="Green", b="Blue")
    async def edit_role(interaction: discord.Interaction, role: discord.Role, name: str, r: int, g: int, b: int):
        await f(bot, interaction, 11, role_id=role.id, name=name, color=discord.Color.from_rgb(r, g, b).value)

    bot.tree.add_command(role_g)