import discord
from discord.ext import commands
from src.config import TOKEN

cogs = [
    "src.cogs.EntertainmentCommands",
    "src.cogs.RoleCommands",
    "src.cogs.EconomyCommands",
    "src.cogs.ModerationCommands",
    "src.cogs.WelcomeCommands",
    "src.cogs.LogCommands",
    "src.cogs.ErrorHandler"
]

class MyBot(commands.Bot):
    def __init__(self, *args,**kargs):
        super().__init__( *args,**kargs)

    async def setup_hook(self):
        for cog in cogs:
            await self.load_extension(cog)
        print("added commands")
        synced = await self.tree.sync()
        print(f"synced {len(synced)} commands")

    async def on_ready(self):
        print("Bot is up")

def run_bot():
    intents = discord.Intents.all()
    bot = MyBot(command_prefix='!', intents=intents)

    @bot.command()
    async def shutdown(ctx:commands.context):
        await ctx.send("Closing")
        await bot.close()
        
    bot.run(TOKEN)
