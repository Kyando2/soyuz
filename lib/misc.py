import os 
from discord.ext import commands

from lib.consts import CONSTS

def token(): 
    return os.environ["discord_token"]

async def channel(bot: commands.Bot):
    return await bot.get_guild(CONSTS.guild).fetch_channel(CONSTS.vote)
