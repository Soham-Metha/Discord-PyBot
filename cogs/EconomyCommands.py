import discord
from discord import app_commands
from discord.ext import commands
import json
import random
import UsefulMethods

items=[
        {"name": "Cookie", "price": 20, "description": "Food"},
        {"name": "Watch", "price": 200, "description": "Time"},
        {"name": "Laptop", "price": 2000, "description": "Work"},
        {"name": "PC", "price": 5000, "description": "Game"}
      ]

class EconomyCommands(commands.Cog):

    def __init__(self,bot = commands.Bot) :
        self.bot = bot

    @app_commands.command()
    async def balance(self,interaction: discord.Interaction, member: discord.Member = None):

        user = interaction.user if member == None else member

        bal = await get_user_bal( str( user.id ) )

        em = discord.Embed( 
            title= f"{user.display_name}'s balance",
            color= discord.Color.red() 
        )

        em.add_field(
            name="Wallet", 
            value=bal[0]
        )

        em.add_field(
            name="Bank", 
            value=bal[1]
        )

        await interaction.response.send_message(embed=em)

    @app_commands.command()
    async def beg(self,interaction: discord.Interaction):
        """
        beg the devs to give you sum $$
        """
        earnings = random.randrange(1001)
        await update_user_bal(str(interaction.user.id), earnings)
        await interaction.response.send_message(f"The dev gave you {earnings} coins!!")

    @app_commands.command()
    async def withdraw(self,interaction: discord.Interaction, amount: int):
        """
        withdraw $$$ from yo bank
        """
        bal = await get_user_bal(str(interaction.user.id)) 

        if amount > bal[1]:
            await interaction.response.send_message("check your bank balance first idiot")
            return

        await update_user_bal(str(interaction.user.id), amount)
        await update_user_bal(str(interaction.user.id), -1 * amount, "bank")
        await interaction.response.send_message(f"you withdrew {amount} coins")

    @app_commands.command()
    async def deposit(self,interaction: discord.Interaction, amount : int):
        """
        deposit $$$ into your bank
        """
        bal = await get_user_bal(str(interaction.user.id))

        if amount > bal[0]:
            await interaction.response.send_message("check your wallet balance first idiot")
            return

        await update_user_bal(str(interaction.user.id), -1 * amount)
        await update_user_bal(str(interaction.user.id), amount, "bank")
        await interaction.response.send_message(f"you deposited {amount} coins")

    @app_commands.command()
    async def send(self,interaction: discord.Interaction, member: discord.Member, amount : int):
        """
        send $$$ to someone
        """
        bal = await get_user_bal(str(interaction.user.id))

        if amount > bal[0]:
            await interaction.response.send_message("check your balance first idiot")
            return

        if amount < 0:
            await interaction.response.send_message("you are an idiot")
            return

        await update_user_bal(str(interaction.user.id), -1 * amount)
        await update_user_bal(str(member.id), amount)
        await interaction.response.send_message(f"you gave {amount} coins to {member}")

    @app_commands.command()
    async def slots(self,interaction: discord.Interaction, amount : int):
        """
        Gamble with yo coins
        """
        bal = await get_user_bal(str(interaction.user.id))

        if amount > bal[0]:
            await interaction.response.send_message("check your wallet balance first idiot")
            return

        if amount <= 0:
            await interaction.response.send_message("you are an idiot")
            return

        final = []
        for i in range(3):
            a = random.choice(["1", "2", "3", "4", "5", "6", "7"])
            final.append(a)

        if final[0] == final[1] == final[2]:
            await update_user_bal(str(interaction.user.id), 3 * amount)
            embed= await UsefulMethods.create_embed(
                title="$$$$$", 
                desc=f"{str(final)}\nDayum son, you won {3 * amount} coins"
            )
            await interaction.response.send_message(embed=embed)

        elif final[0] == final[1] or final[2] == final[1] or final[0] == final[2]:
            await update_user_bal(str(interaction.user.id), 2 * amount)
            embed= await UsefulMethods.create_embed(
                title="$$$", 
                desc=f"{str(final)}\nYour luck's good today,you won {2 * amount} coins"
            )
            await interaction.response.send_message(embed=embed)
        else:
            await update_user_bal(str(interaction.user.id), -1 * amount)
            embed= await UsefulMethods.create_embed(
                title="TT", 
                desc=f"{str(final)}\ntry again, you might just hit the jackpot"
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def rob(self,interaction: discord.Interaction, member: discord.Member):
        """
        rob a user
        """
        robber_bal = await get_user_bal(str(interaction.user.id))
        user_bal = await get_user_bal(str(member.id))

        if robber_bal[0] < 1000:
            await interaction.response.send_message("check your balance first idiot")
            return

        if user_bal[0] < 1000:
            await interaction.response.send_message("don't you feel embarrassed trying to rob that poor fella?")
            return

        amount = random.randrange(-1 * robber_bal[0], user_bal[0])
        await update_user_bal(str(interaction.user.id), amount)
        await update_user_bal(str(member.id), -1 * amount)
        if amount < 0:
            await interaction.response.send_message(f"you suck at robbing,you gave {amount} coins to {member.mention} as an apology")
        else:
            await interaction.response.send_message(f"you successfully stole {amount} coins from {member.mention}")

    @app_commands.command()
    async def shop(self,interaction: discord.Interaction):
        """
        check the items available in the shop
        """
        em = discord.Embed(title="Shop",color=discord.Colour.blurple())
        for item in items:
            name = item["name"]
            price = item["price"]
            description = item["description"]
            em.add_field(name=name, value=f"${price} | {description} ", inline=False)

        await interaction.response.send_message(embed=em)

    @app_commands.command()
    async def buy(self,interaction: discord.Interaction, item:str, amount:int=1):
        """
        buy an item from the shop
        """
        res = await buy_this(interaction.user, item, amount)

        if not res[0]:
            if res[1] == 1:
                await interaction.response.send_message("That Object isn't there!")
                return
            if res[1] == 2:
                await interaction.response.send_message(f"You don't have enough money in your wallet to buy {amount} {item}")
                return

        await interaction.response.send_message(f"You just bought {amount} {item}")

    @app_commands.command()
    async def bag(self,interaction: discord.Interaction):
        """
        check your bag
        """
        try:
            inv = (await get_user_bal(user_id=str(interaction.user.id)))[2]
        except:
            inv = []

        em = discord.Embed(title="Inventory")
        for item in inv:
            name = item["item"]
            amount = item["amount"]
            em.add_field(name=name, value=amount)

        await interaction.response.send_message(embed=em)

    @app_commands.command()
    async def sell(self,interaction: discord.Interaction, item:str, amount:int=1):
        """
        sell an item from your bag
        """
        res = await sell_this(interaction.user, item, amount)
        if not res[0]:
            if res[1] == 1:
                await interaction.response.send_message("That Object isn't there!")
                return
            if res[1] == 2:
                await interaction.response.send_message(f"You don't have {amount} {item} in your bag.")
                return
            if res[1] == 3:
                await interaction.response.send_message(f"You don't have {item} in your bag.")
                return

        await interaction.response.send_message(f"You just sold {amount} {item}.")

    @app_commands.command()
    async def dev_send(self,interaction: discord.Interaction, member: discord.Member, amount:int):
        if str(interaction.user.id) == "637848977290559538":
            await update_user_bal(str(member.id), amount)
            await interaction.response.send_message(f"added/decreased the balance of {member} by {amount}")
        else:
            await interaction.response.send_message("This only works if you are the dev,Idiot")

async def sell_this(user, item_name, amount, price=None):
    """
    decrease `amount` number of `item`s to `user`'s bag and increment his balance as per the item price(at a 10% lower price)
    """
    item_name = item_name.lower()
    Item_check = None
    for item in items:
            name = item["name"].lower()
            if name == item_name:
                Item_check = name
                if price is None:
                    price = 0.9 * item["price"]
                break

    #Check if the item specified exists
    if Item_check is None:
            return [False, 1]

    cost = price * amount
    users = await get_all_data()
    bal = await get_user_bal(str(user.id))

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t is None:
            return [False, 3]
    except:
        return [False, 3]

    await save_all_data(users=users)
    await update_user_bal(str(user.id), cost, "wallet")
    return [True, "Worked"]

async def buy_this(user : discord.Member, item:str, amount:int):
    """
    add `amount` number of `item`s to `user`'s bag and decrement his balance as per the item price
    """
    item_name = item.lower()
    item_check = None

    # Checks if the item exists in the Shop
    for item in items:
        name = item["name"].lower()
        if name == item_name:
            item_check = name
            price = item["price"]
            break
        
    # If item doesn't exist , return code 1
    if item_check is None:
        return [False, 1]

    cost = price * amount
    users = await get_all_data()
    bal = await get_user_bal(str(user.id))

    # If user does't have enough money , return code 2
    if bal[0] < cost:
        return [False, 2]

    # To add the item to the bag 
    # if user already has the item , increase the item quantity
    # otherwise append the item to the bag
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t is None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    await save_all_data(users=users)

    await update_user_bal(str(user.id), cost * -1, "wallet")

    return [True, "No Error"]

async def open_account(user_id:str):
    """
    initializes the balance of new users\n
    returns `false` if user account is already present\n
    returns `true` if user account is successfully created
    """
    users = await get_all_data()
    if user_id in users:
        return False
    users[user_id] = {}
    users[user_id]["wallet"] = 69
    users[user_id]["bank"] = 420
    users[user_id]["bag"] = []
    await save_all_data(users=users)
    return True

async def get_all_data():
    """
    returns the data saved in `userdata.json`
    """
    with open("userdata.json", "r") as f:
        users = json.load(f)
    return users

async def save_all_data(users):
    """
    saves the data passed to `userdata.json`
    """
    with open("userdata.json", "w") as f:
        json.dump(users, f,indent=4)

async def get_user_bal(user_id:str ):
    """
    returns the balance of the user\n
    `[0]` = wallet\n
    `[1]` = bank\n
    `[2]` = bag
    """
    await open_account(user_id=user_id)
    users = await get_all_data()
    bal = users[user_id]["wallet"], users[user_id]["bank"], users[user_id]["bag"]
    return bal

async def update_user_bal(user_id : str, change:int, mode:str="wallet"):
    """
    increases/decreases the balance of the user\n
    operation is performed on `wallet` by default\n
    returns the balance of the user\n
    `[0]` = wallet\n
    `[1]` = bank\n
    `[2]` = bag
    """
    await open_account(user_id=user_id)
    users = await get_all_data()
    users[user_id][mode] += change
    await save_all_data(users=users)
    bal = [users[user_id]["wallet"], users[user_id]["bank"]], users[user_id]["bag"]
    return bal

async def setup(bot : commands.Bot):
    await bot.add_cog(EconomyCommands(bot=bot))