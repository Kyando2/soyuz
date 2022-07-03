from discord.utils import MISSING
from discord.ext import commands
class Action(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            j = v if v != None else None
            self.__setattr__(k, j)
    async def run(self, bot: commands.Bot):
        pass
    def ID(self):
        pass
    def as_dict(self):
        pass
    def msg(self):
        pass