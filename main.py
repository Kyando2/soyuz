from discord.ext import commands

from lib.misc import token
from lib.permanent import PermanentJsonContext

import discord

pj = PermanentJsonContext("test")

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = Bot()

bot.run(token())
