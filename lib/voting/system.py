import discord
from discord.ext import commands
import uuid

from lib.permanent import PermanentJsonContext
from lib.voting.actions.channel_actions import CreateTextChannelAction, DeleteChannelAction, PurgeChannelAction
from lib.consts import CONSTS
from lib.misc import channel
from lib.voting.actions.action import Action
from lib.voting.actions.message_actions import DeleteMessageAction, SendMessageAction

ACTION_DICT = {
    0: CreateTextChannelAction,
    1: DeleteChannelAction,
    2: SendMessageAction,
    3: DeleteMessageAction,
    4: PurgeChannelAction
}

def action_factory(id, **kwargs):
    return ACTION_DICT[id](
        **kwargs
    )

class Vote(discord.ui.View):
    def __init__(self, action: Action, count, threshold, message_id, bot, id):
        super().__init__(timeout=None)
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
                "a_v": {} ,
                "count": self.count,
                "threshold": self.threshold,
                "action": action.get_id(),
                "message_id": self.message_id,
                "action_d": action.as_dict()
            }

    async def check(self):
        ch = await channel(self.bot)
        msg = await ch.fetch_message(self.message_id)
        if self.count >= self.threshold:
            await self.action.run(self.bot)
            await ch.send("Vote passed.", reference=msg)
            self.can_vote = False
        elif self.count <= -self.threshold:
            await ch.send("Vote rejected.", reference=msg)
            self.can_vote = False
        
    async def pressed(self, value, id):
        ov = value
        msg = ""
        value = self.can_votef(id, value)
        if value != 0:
            msg = "Sucessfully voted."
            self.count+=value
            await self.check()
            self.updatev(id, value/abs(value))
        else:
            if self.can_vote == False:
                msg = "This vote is over."
            else:
                msg = f'You have already voted { "for" if ov > 0 else "against" }.'
        self.update()
        return msg

    def can_votef(self, id, v):
        pj = PermanentJsonContext("votes")
        if not self.can_vote: return False
        if str(id) in pj[self.id]["a_v"].keys():
            if v != int(pj[self.id]["a_v"][str(id)]):
                return v*2
            else:
                return 0
        else:
            return v

    def update(self):
        pj = PermanentJsonContext("votes")
        pj[self.id]["count"] = self.count
        pj[self.id]["message_id"] = self.message_id
        pj.update()
    
    def updatev(self, id, v):
        pj = PermanentJsonContext("votes")
        pj[self.id]["a_v"][id] = v
        pj.update()


    def raw_update(self):
        pj = PermanentJsonContext("votes")
        pj[self.id]["count"] = self.count
        pj[self.id]["message_id"] = self.message_id
        pj.update()

def vote_factory(action: Action, count, threshold, message_id, bot, id=None):
    id = id if id != None else str(uuid.uuid4())
    class Temp(Vote):
        def __init__(self, action: Action, count, threshold, bot, message_id):
            super().__init__(action, count, threshold, message_id, bot, id)

        @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, custom_id=f'{ id }:yes')
        async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
            msg = await self.pressed(1, interaction.user.id)
            await interaction.response.send_message(msg, ephemeral=True)

        @discord.ui.button(label='No', style=discord.ButtonStyle.red, custom_id=f'{ id }:no')
        async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
            msg = await self.pressed(-1, interaction.user.id)
            await interaction.response.send_message(msg, ephemeral=True)   

    return Temp(action, count, threshold, bot, message_id)


async def vote(bot: commands.Bot, interaction: discord.Interaction, id, **kwargs):
    action = action_factory(id, **kwargs)
    vote = vote_factory(action, 0, CONSTS.threshold, 0, bot)
    vch = await channel(bot)
    x = discord.Embed(title="Vote", description=action.message(), type="rich", color=0xbf0606)
    msg = await vch.send(embed=x, view=vote)
    vote.message_id = msg.id
    vote.raw_update()
    await interaction.response.send_message("Successfully created vote.", ephemeral=True)
