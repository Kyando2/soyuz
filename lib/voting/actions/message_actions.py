from discord.ext import commands
from typing import Optional
from lib.misc import guild
from discord.utils import MISSING
from discord import app_commands
import discord
from lib.voting.actions.action import Action

class SendMessageAction(Action):
    ID = 2

    def __init__(self, channel_id, text):
        super().__init__(channel_id=channel_id, text=text)

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        ch = await gu.fetch_channel(self.channel_id)
        await ch.send(self.text)

    def message(self):
        return f'Proposal to send the message `"{ self.text }"` to channel the <#{ self.channel_id }>.'

def register_message_actions(bot: commands.Bot, f):
    message_g = app_commands.Group(name="message", description="actions related to messages")

    @message_g.command(name="send")
    @app_commands.describe(channel="The name of the channel you want to send the message to", text="The message you want to send",)
    async def send_message(interaction: discord.Interaction, channel: discord.abc.GuildChannel, text: str):
        await f(bot, interaction, 2, channel_id=channel.id, text=text)


    bot.tree.add_command(message_g)