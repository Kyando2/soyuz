from discord.ext import commands
from lib.consts import CONSTS
from lib.misc import guild
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

class DeleteMessageAction(Action):
    ID = 1

    def __init__(self, channel_id, message_id):
        super().__init__(channel_id=channel_id, message_id=message_id)
    
    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        ct = await gu.fetch_channel(self.channel_id)
        mg = await ct.fetch_message(self.message_id)
        await mg.delete()
    
    def message(self):
        return f'Proposal to delete a message in <#{ self.channel_id }>\n[Message link](https://discord.com/channels/969011076144431165/{self.channel_id}/{self.message_id})'

def register_message_actions(bot: commands.Bot, f):
    message_g = app_commands.Group(name="message", description="actions related to messages")

    @message_g.command(name="send")
    @app_commands.describe(channel="The name of the channel you want to send the message to", text="The message you want to send",)
    async def send_message(interaction: discord.Interaction, channel: discord.abc.GuildChannel, text: str):
        if channel.id in CONSTS.notouch:
            await interaction.response.send_message(f'You cannot send messages to <#{ channel.id }>.', ephemeral=True)
        else:
            await f(bot, interaction, 2, channel_id=channel.id, text=text)
    
    @message_g.command(name="nonthread")
    @app_commands.describe(channel="The channel in which the message is", message_id="The message to delete")
    async def delete_channel(interaction: discord.Interaction, channel: discord.abc.GuildChannel, message_id: str):
        if channel.id in CONSTS.notouch:
            await interaction.response.send_message(f'You cannot delete a message in <#{ channel.id }>.', ephemeral=True)
        else:
            await f(bot, interaction, 1, channel_id=channel.id, message_id=message_id)


    bot.tree.add_command(message_g)