import discord
from discord.ext import commands
from discord import app_commands
import src.GuildDataAccessCommands

class LogCommands(commands.Cog):

    def __init__(self,bot = commands.Bot) :
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel: discord.abc.GuildChannel):
        em = discord.Embed(
            title="Created a channel", 
            description= f" created the channel {channel.mention}"
        )
        await GuildDataAccessCommands.log(bot=self.bot,guild_id=str(channel.guild.id),embed=em,mode="Logs")

    @app_commands.command()
    async def setlogschannel(self,interaction: discord.Interaction, channel : discord.TextChannel):
        """
        Set the channel which will record the various changes made to the guild
        """
        await GuildDataAccessCommands.set_channel(
            interaction=interaction,
            channel=channel,
            mode="Logs"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(LogCommands(bot=bot))
