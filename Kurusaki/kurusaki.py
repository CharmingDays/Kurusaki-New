import discord,asyncio,os
from discord import permissions
from discord.ext import commands
from discord.ext import tasks
import random
from dotenv import load_dotenv
import pymongo
load_dotenv()



extensions=[
    'Cogs.API.channels',
    'Cogs.API.help',
    # 'Cogs.API.events',
    'Cogs.API.guild',
    'Cogs.Fun.lava'
    ]


def load_cogs():
    for ext in extensions:
        bot.load_extension(ext)


client = pymongo.MongoClient(os.getenv("MONGO"))
gen_collection = client['Discord-Bot-Database']['General']

def load_status():
    global bot_status
    bot_status = gen_collection.find_one({'_id':'bot_status'})['kurusaki']
    client.close()


def load_custom_prefix():
    global server_prefixes
    server_prefixes = gen_collection.find_one({'_id':'bot_prefixes'})
    server_prefixes.pop('_id')
    client.close()


async def refresh_prefixes(Id,newPrefix):
    if Id in server_prefixes:
        server_prefixes[Id].append(newPrefix)

    if Id not in server_prefixes:
        server_prefixes[Id] = [newPrefix]
    
def get_prefix(bot, msg):
    prefixes = ['s.']
    if msg.guild.id is None: #NOTE  Inside DM
        return commands.when_mentioned_or(*prefixes)(bot, msg)


    if msg.guild.id == 264445053596991498: 
        #TOP.GG
        return commands.when_mentioned_or(*['s.'])(bot, msg)

    if str(msg.guild.id) in server_prefixes:
        return commands.when_mentioned_or(*server_prefixes[str(msg.guild.id)])(bot,msg)

    
    return commands.when_mentioned_or(*prefixes)(bot, msg) #NOTE if server not in database


bot = commands.Bot(command_prefix=get_prefix,description='A multipurpose discord bot',case_insensitive=True,owner_id=185181025104560128)


async def change_interval():
    timer=random.randint(10,360)
    status_changer.change_interval(minutes=timer)


@tasks.loop(minutes=random.randint(5,360))
async def status_changer():
    types = [['game',0],['music',2],['watch',3]]
    ran =random.choice(types)
    current_active = discord.Activity(name=random.choice(bot_status[ran[0]]), type=ran[1])
    await bot.change_presence(activity=current_active)
    await change_interval()



async def first_status():
    types = [['game',0],['music',2],['watch',3]]
    ran =random.choice(types)
    current_active = discord.Activity(name=random.choice(bot_status[ran[0]]), type=ran[1])
    await bot.change_presence(activity=current_active)




@bot.event
async def on_ready():
    status_changer.start()
    await first_status()
    print(f"discord.py -- {discord.__version__}")
    print(f"{bot.user.name} is ready to run!")
    load_cogs()



@bot.event
async def on_disconnect():
    status_changer.stop()


@bot.event
async def on_command(msg):
    if str(msg.guild.id) not in server_prefixes:
        server_prefixes[str(msg.guild.id)] = ['s.']



@commands.has_permissions(administrator=True)
@bot.command(name='add-prefix',hidden=True,enabled=False)
async def add_prefix(msg,*,prefix:str = None):
    """
    Add a custom server prefix
    `CMD`: add-prefix(new_prefix:Required)
    `Ex`: s.add-prefix !a.
    `Permissions`: Administrator
    """

    if prefix is None:
        return await msg.send("Please enter a prefix with the command. Type `s.help add-prefix` for command docs")

    if str(msg.guild.id) in server_prefixes:
        if prefix in server_prefixes[str(msg.guild.id)]:
            return await msg.send(f"Server prefix `{prefix}` already in database")
        
        if len(server_prefixes[str(msg.guild.id)]) > 3:
            return await msg.send(f"Only premium members can have more than 2 custom server prefixes.\nYou can use s.remove-prefix on the default prefix.\nUse command `s.premium` to find out how to get premium.")

        else:
            server_prefixes[str(msg.guild.id)].append(prefix)
            gen_collection.update_one({'_id':'bot_prefixes'},{'$addToSet':{str(msg.guild.id):{"$each":[prefix,'s.']}}})
            return await msg.send(f"New prefix `{prefix}` added to server.")
            
    
    if str(msg.guild.id) not in server_prefixes:
        gen_collection.update_one({'_id':'bot_prefixes'},{'$addToSet':{str(msg.guild.id):{"$each":[prefix,'s.']}}})
        server_prefixes[str(msg.guild.id)]= [prefix]

        return await msg.send(f"New prefix `{prefix}` added to server.")


@commands.has_permissions(administrator=True)
@bot.command(name='del-prefix',aliases=['remove-prefix'],hidden=True,enabled=False)
async def remove_prefix(msg,*,prefix:str = None):
    """
    remove a custom or default bot prefix for your server
    `CMD`: remove-prefix(current_prefix:Required)
    `Ex`: s.del-prefix !a.
    `Permissions`: Administrator
    """
    if prefix is None:
        return await msg.send("Please enter a prefix to remove with the command. Use `s.del-prefix` to view the docs")

    if str(msg.guild.id) not in server_prefixes:
        server_prefixes[str(msg.guild.id)] = ['s.']
        await msg.send("Something went wrong while trying to add the command, please try again later.")
    
    if str(msg.guild.id) in server_prefixes:
        if prefix not in server_prefixes[str(msg.guild.id)]:
            return await msg.send(f"Prefix `{prefix}` not found")

        if len(server_prefixes[str(msg.guild.id)]) == 1:
            return await msg.send("You can not remove the last prefix because the bot requires at least one prefix")
        
        try:
            server_prefixes[str(msg.guild.id)].remove(prefix)
            gen_collection.update_one({'_id':'bot_prefixes'},{'$pull':{str(msg.guild.id):prefix}})
            return await msg.send(f"Prefix `{prefix}` has been removed.")
        except KeyError:
            return await msg.send(f"Prefix `{prefix}` not found.")



@bot.command()
async def prefixes(msg):
    if str(msg.guild.id) in server_prefixes:
        return await msg.send(f"{msg.guild.name}'s prefixe(s):  {', '.join(server_prefixes[str(msg.guild.id)])}")
    
    return await msg.send(f"{msg.guild.name}'s prefixe(s): s.")




@bot.command()
async def premium(msg):
    """
    Tells you how to get premium  for Kurusaki
    `CMD`: premium()
    `Ex`: s.premium
    """
    pass






load_status()
load_custom_prefix()

bot.run(os.getenv('TOKEN'),reconnect=True)