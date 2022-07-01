from typing import Optional

from discord.ext import commands
from discord import app_commands
from lib.misc import token
from lib.permanent import PermanentJsonContext
from lib.voting.system import vote_factory, action_factory
from lib.consts import CONSTS

import discord

MY_GUILD = discord.Object(CONSTS.guild)

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self):
        pj = PermanentJsonContext("votes")
        for k in pj.structure.keys():
            c = pj[k]
            action = action_factory(c["action"], **c["action_d"])
            self.add_view(vote_factory(action, c["count"], c["threshold"], c["message_id"], k))
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

bot = Bot()

@bot.tree.command()
@app_commands.describe(
    name="The name of the channel you want to create",
    category="The category you want to add the channel to",
)
async def create_channel(interaction: discord.Interaction, name: str, category: Optional[discord.CategoryChannel]):
    action = action_factory(0, name=name, category=category)

bot.run(token())
