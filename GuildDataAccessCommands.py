import json
import discord
from discord.ext import commands

modes = ["Welcome","Exit","Logs"]

async def get_Guild_data():
    """
    returns all the data stored in `guilddata.json`
    """
    with open("guilddata.json", "r") as f:
        guilds = json.load(f)
    return guilds

async def save_Guild_data(guilds):
    """
    writes the data passed to the `guilddata.json` 
    """
    with open("guilddata.json", "w") as f:
        json.dump(obj = guilds,fp = f,indent=4)

async def set_init_vals(guild_id:str):
    """
    sets the inital channels of all modes to `Not Set`\n
    `modes` = `Welcome`, `Exit`, `Logs`\n
    returns `False` if the values are already set and `True` otherwise
    """
    guilds = await get_Guild_data()
    if guild_id in guilds :
        return False
    guilds[guild_id] = {}
    for m in modes:
        guilds[guild_id][m] = None
    await save_Guild_data(guilds=guilds)
    return True

async def get_channel(guild_id:str, mode: str = "Welcome"):
    """
    returns the channel associated with the `mode` for a paricular guild\n
    `modes = "Welcome", "Exit", "Logs"`
    """
    guilds = await get_Guild_data()
    return str(guilds[guild_id][mode])

async def set_channel(interaction:discord.Interaction,channel:discord.TextChannel,mode:str):
    """
    updates the `channel` associated with the `mode` for a paricular guild and sends a message stating the same through the `interaction`\n
    `modes = "Welcome", "Exit", "Logs"`
    """
    guild_id=str(interaction.guild_id)
    channel_id=str(channel.id)

    await set_init_vals(guild_id=guild_id)
    
    await interaction.response.send_message(f"set {channel.mention} as the {mode} channel")

    guilds = await get_Guild_data()
    guilds[guild_id][mode] = channel_id
    await save_Guild_data(guilds=guilds)

async def log(bot:commands.Bot,guild_id: str,message:str=None,embed:discord.Embed=None,mode:str = "Welcome"):
    """
    Send a `message`/`embed` in the `mode` channel of a particular `guild` to show an action performed in it\n
    `bot` = the bot throught which the message will be sent\n
    `guild_id` = the guild in which the action is performed\n
    `message`/`embed`= the message/embed that is to be sent\n
    `mode` = decides the channel in which the message is sent\n
    returns `False` if channel not set and `True` otherwise\n
                    NOTE : mode is set to the Welcome channel by default
    """
    channel_id = await get_channel(guild_id=guild_id,mode=mode)
    # returns False if channel not set
    if channel_id == None:
        return False

    channel = bot.get_channel(int(channel_id))
    # returns if the channel specified doesn't exist (it was deleted / bot doesn't have access to it)
    if not channel:
        return False

    if embed != None:
        await channel.send(embed=embed)
    elif message != None:
        await channel.send(message)
    else:
        await channel.send("some idiot(dev) didn't specify the content to be sent")
    return True
