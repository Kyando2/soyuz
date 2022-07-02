from re import M
import discord
import uuid

from lib.permanent import PermanentJsonContext
from lib.consts import CONSTS
from lib.misc import channel

class Action(object):
    def __init__(self):
        pass
    async def run(self):
        pass
    def ID(self):
        pass
    def as_dict(self):
        pass
    

ACTION_DICT = {
    
}

def action_factory(id, **kwargs):
    return ACTION_DICT[id](
        **kwargs
    )

class Vote(discord.ui.View):
    def __init__(self, action: Action, count, threshold, message_id, bot, id):
        super().__init__()
        self.action = action
        self.count = count
        self.threshold = threshold
        self.bot = bot
        self.can_vote = True
        self.message_id = message_id
        self.id = id
        pj = PermanentJsonContext("votes")
        if self.id not in pj:
            pj[self.id] = {
                "a_v": [] ,
                "count": self.count,
                "threshold": self.threshold,
                "action": action.ID(),
                "message_id": self.message_id,
                "action_d": action.as_dict()
            }

    async def check(self):
        ch = await channel(self.bot)
        msg = await ch.fetch_message(self.message_id)
        if self.count > self.threshold:
            await self.action.run()
            await ch.send("Vote passed.", reference=msg)
            self.can_vote = False
        elif self.count < -self.threshold:
            await ch.send("Vote rejected.", reference=msg)
            self.can_vote = False
        
    async def pressed(self, value, id):
        msg = ""
        if self.can_vote(id):
            msg = "Sucessfully voted."
            self.count+=value
            await self.check()
        else:
            if self.can_vote == False:
                msg = "This vote is over."
            else:
                msg = "You have already voted."
        self.update(id)
        return msg

    def can_vote(self, id):
        pj = PermanentJsonContext("votes")
        if not self.can_vote: return False
        else: return not (id in pj[self.id]["a_v"])

    def update(self, id):
        pj = PermanentJsonContext("votes")
        pj[self.id]["count"] = self.count
        pj[self.id]["a_v"].append(id)
        pj[self.id]["message_id"] = self.message_id
        pj.update()

def vote_factory(action: Action, count, threshold, message_id, bot, id=None):
    id = id if id != None else uuid.uuid4()
    class Temp(Vote):
        def __init__(self, action: Action, count, threshold, bot, message_id):
            super().__init__(action, count, threshold, message_id, bot, id)

        @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, custom_id=f'{ id }:yes')
        async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
            msg = await self.pressed(1)
            await interaction.response.send_message(msg, ephemeral=True)

        @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, custom_id=f'{ id }:yes')
        async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
            msg = await self.pressed(-1)
            await interaction.response.send_message(msg, ephemeral=True)   

    return Temp(action, count, threshold, bot, message_id)