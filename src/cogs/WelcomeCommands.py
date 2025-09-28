import discord
from discord import app_commands
from discord.ext import commands
import src.GuildDataAccessCommands

class WelcomeCommands(commands.Cog):

    def __init__(self,bot = commands.Bot) :
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        await GuildDataAccessCommands.log(
            bot=self.bot,
            guild_id=str(member.guild.id),
            message=f"Welcome {member.mention}, you are the {member.guild.member_count}th member of {member.guild.name}."
        )

    @commands.Cog.listener()
    async def on_member_remove(self,member:discord.Member):
        await GuildDataAccessCommands.log(
            bot=self.bot,
            guild_id=str(member.guild.id),
            message=f"Bye {member.mention}, you won't be missed. \n{member.guild.name} is down to {member.guild.member_count} members.",
            mode="Exit"
        )

    @app_commands.command()
    async def setwelcomechannel(self,interaction: discord.Interaction, channel : discord.TextChannel):
        """
        Set the channel in which a message will be sent when a member joins the server
        """
        await GuildDataAccessCommands.set_channel(
            interaction=interaction,
            channel=channel,
            mode="Welcome"
        )

    @app_commands.command()
    async def setexitchannel(self,interaction: discord.Interaction,channel : discord.TextChannel):
        """
        Set the channel in which a message will be sent when a member leaves the server
        """
        await GuildDataAccessCommands.set_channel(
            interaction=interaction,
            channel=channel,
            mode="Exit"
        )

async def setup(bot : commands.Bot):
    await bot.add_cog(WelcomeCommands(bot=bot))
