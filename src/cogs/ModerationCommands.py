import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class mod(commands.Cog):

    def __init__(self,bot = commands.Bot) :
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_messages(self,interaction:discord.Interaction,amount:int):
        """
        purge `amount` messages
        """
        await interaction.response.defer(thinking=True)
        await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"{interaction.user}deleted {amount} messages")

    @app_commands.command()
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self,interaction: discord.Interaction, member: discord.Member, reason:str):
        """
        kick a member from the server
        """
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member} has been kicked for {reason}")

    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self,interaction: discord.Interaction, member: discord.Member, reason:str):
        """
        ban a member from the server
        """
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member} has been banned for {reason}")
        
    @app_commands.command()
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self,interaction: discord.Interaction, member: discord.Member, reason:str):
        """
        warn a member of the server
        """
        await interaction.response.send_message(f"{member.mention()} has been warned for {reason}")
        
    @app_commands.command()
    @app_commands.checks.has_permissions(kick_members=True)
    async def dm(self,interaction: discord.Interaction, member: discord.Member, message:str):
        """
        DM a member of the server
        """
        await member.send(message)
        await interaction.response.send_message(f"'{message}' has been sent to {member}")
        
    @app_commands.command()
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self,interaction: discord.Interaction, member: discord.Member, minutes: int, reason:str):
        """
        timeout a member of the server
        """
        time = timedelta(minutes=minutes)
        await member.timeout(time,reason=reason)
        await interaction.response.send_message(f"{member} has been timed out for {time} \nreason = {reason}")

async def setup(bot : commands.Bot):
    await bot.add_cog(mod(bot=bot))
