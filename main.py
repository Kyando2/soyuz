from discord.ext import commands

from lib.misc import token
from lib.permanent import PermanentJsonContext

import discord

pj = PermanentJsonContext("test")

print(pj.v)

