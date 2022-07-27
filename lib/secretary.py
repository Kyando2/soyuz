from discord.ext import commands
from lib.misc import guild, token
from lib.permanent import PermanentJsonContext
from lib.voting.actions.vote import register_actions
from lib.voting.system import vote_factory, action_factory, vote
from lib.consts import CONSTS

import discord

MY_GUILD = discord.Object(CONSTS.guild)

class Secretary(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)
        register_actions(self, vote)
        self.run(token())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        gu = guild(self)
        ch = await gu.fetch_channel(970419838604439642)
        await ch.send("Bot restarted.")

    async def on_message(self, message):
        if message.guild == None and await self.is_owner(message.author):
            gu = guild(self)
            ch = await gu.fetch_channel(970419838604439642)
            await ch.send(message.content)

    async def setup_hook(self):
        pj = PermanentJsonContext("votes")
        for k in pj.structure.keys():
            c = pj[k]
            action = action_factory(c["action"], **c["action_d"])
            self.add_view(vote_factory(action, c["count"], c["threshold"], c["message_id"], self, k))
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)