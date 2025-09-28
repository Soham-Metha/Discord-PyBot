import discord
from discord import app_commands
from discord.ext import commands
import src.UsefulMethods

class EntertainmentCommands(commands.Cog):

    def __init__(self,bot = commands.Bot) :
        self.bot = bot

    @app_commands.command()
    async def server_link(self,interaction:discord.Interaction):
        """
        get a link to the Community server
        """
        em = discord.Embed(title="Discord server",description="https://discord.gg/EDzPnzrCUB",colour=discord.Colour.random())
        em.set_thumbnail(url= "https://i.redd.it/3h830ttao8341.jpg")
        await interaction.response.send_message(embed=em)

    @app_commands.command()
    async def pfp(self,interaction:discord.Interaction,member: discord.Member = None):
        """
        get the profile picture of a user
        """
        member = interaction.user if member == None else member
        em     = discord.Embed(title=f"{member.display_name}'s Profile picture", colour=discord.Colour.random())
        em.set_image(url= f"{member.display_avatar}")
        await interaction.response.send_message(embed=em)

    @app_commands.command()
    async def custom_embed(
        self,
        interaction: discord.Interaction,
        title:str,desc: str,
        url: str=None, 
        author: discord.Member = None,
        image:str=None,
        thumbnail:str=None,
        footer_img:str=None,
        footer_text:str=None
    ):
        """
        create an embed according to your own requirements
        """
        embed= UsefulMethods.create_embed(
            title      = title, 
            desc       = desc,
            url        = url, 
            author     = author, 
            image      = image, 
            thumbnail  = thumbnail,
            footer_img = footer_img, 
            footer_text= footer_text
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot : commands.Bot):
    await bot.add_cog(EntertainmentCommands(bot=bot))
