import discord
from discord import app_commands
from discord.ext import commands

em = discord.Embed(title="Select roles",description="<:PepeKMS:717981570329346060> : BrawlStars \n<:stabbo:752384458392338482> : CODM \n <:peepoPANTIES:717981480676229142> : FF \n <:panda_1:730726013289365504> : NFS")

async def addrrole(role: discord.Role,interaction: discord.Interaction):
    user= interaction.user
    if role in [y.id for y in user.roles]:
        await user.remove_roles(user.guild.get_role(role))
        await interaction.response.send_message("role removed",ephemeral=True)
    else:
        await user.add_roles(user.guild.get_role(role))
        await interaction.response.send_message("role added",ephemeral=True)

class RoleButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value= None

    @discord.ui.button( emoji="<:PepeKMS:717981570329346060>" , style= discord.ButtonStyle.blurple)
    async def BrawlStars(self, interaction: discord.Interaction, button: discord.ui.Button):
        role=717010893640040499
        await addrrole(role=role,interaction=interaction)

    @discord.ui.button(emoji="<:stabbo:752384458392338482>", style= discord.ButtonStyle.blurple)
    async def CODM(self, interaction: discord.Interaction, button: discord.ui.Button):
        role=717011819348230195
        await addrrole(role=role,interaction=interaction)
    
    @discord.ui.button(emoji="<:peepoPANTIES:717981480676229142>", style= discord.ButtonStyle.blurple)
    async def FreeFire(self, interaction: discord.Interaction, button: discord.ui.Button):
        role=717011489051115551
        await addrrole(role=role,interaction=interaction)

    @discord.ui.button(emoji="<:panda_1:730726013289365504>", style= discord.ButtonStyle.blurple)
    async def NFS(self, interaction: discord.Interaction, button: discord.ui.Button):
        role=717011034434699306
        await addrrole(role=role,interaction=interaction)

class RoleCommands(commands.Cog):

    def __init__(self,bot = commands.Bot) :
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_em1(self,interaction: discord.Interaction):
        """
        send the embed for selecting roles
        """
        await interaction.response.send_message(embed= em,view=RoleButtons())

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role(self,interaction:discord.Interaction,member:discord.Member,role:discord.Role):
        """
        assign/remove a role from a user
        """
        addrrole(role= role.id,interaction= interaction)

async def setup(bot : commands.Bot):
    await bot.add_cog(RoleCommands(bot=bot))