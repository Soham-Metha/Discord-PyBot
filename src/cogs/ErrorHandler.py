import discord
from discord import app_commands
from discord.ext import commands

class ErrorHandler(commands.Cog):

    def __init__(self,bot = commands.Bot) :
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self,interaction:discord.Interaction,error: app_commands.AppCommandError):
        await interaction.response.send_message(f"There was an error with the command : \n{type(error).__name__}")

    @commands.Cog.listener()
    async def on_command_error(self,ctx : commands.Context,error:commands.CommandError):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You don't have permissions to use this command",ephemeral=True)
        else:
            await ctx.send(f"There was an error with the command : \n{type(error).__name__}")

async def setup(bot : commands.Bot):
    await bot.add_cog(ErrorHandler(bot=bot))
