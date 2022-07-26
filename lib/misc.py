import os 
from discord.ext import commands

from lib.consts import CONSTS

def token(): 
    return os.environ.get("DISCORD_TOKEN", "x")

async def channel(bot: commands.Bot):
    return await bot.get_guild(CONSTS.guild).fetch_channel(CONSTS.vote)

def guild(bot: commands.Bot):
    return bot.get_guild(CONSTS.guild)