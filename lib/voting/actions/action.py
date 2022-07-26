from discord.ext import commands
class Action(object):
    ID = -1

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            j = v if v != None else None
            self.__setattr__(k, j)

        self._dict = kwargs
        
    async def run(self, bot: commands.Bot):
        pass

    def get_id(self):
        return self.ID

    def as_dict(self):
        return self._dict

    def msg(self):
        pass