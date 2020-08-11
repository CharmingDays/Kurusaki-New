import json
import discord,asyncio,os
from discord.ext import commands
from discord.ext.commands import Greedy
from dotenv import load_dotenv
from discord.ext import tasks
import logging,random
load_dotenv()


def get_prefix(bot, msg):

    if msg.guild is not None and msg.guild.id == 264445053596991498:
        return commands.when_mentioned_or(*['k.'])(bot, msg)

    prefixes = ['s.', 'k.']

    return commands.when_mentioned_or(*prefixes)(bot, msg)


bot = commands.Bot(command_prefix=get_prefix,description='A multipurpose discord bot',case_insensitive=True,owner_id=185181025104560128)



listening=discord.ActivityType.listening
watching=discord.ActivityType.watching
playing=discord.ActivityType.playing
bot_statuses=[('SING - Moonlight Thoughts','Twice - Likey',listening), 
('Twice - Knock Knock',listening),('Twice - What is love?',listening),
('T-ara Like The First Time',listening),('Girls Generation - Gee',listening),
('T-ara - Holiday',listening),('League of Legends',playing),('Valorant',playing),
('Overwatch',playing),('Silent Hill',watching),('Dexter',watching),('Supernatural',watching),
('Yanxi Palace',watching)]


async def change_interval():
    timer=random.randint(20,360)
    status_changer.change_interval(seconds=timer)



@tasks.loop(minutes=random.randint(20,360))
async def status_changer():
    random_status=random.choice(bot_statuses)
    current_active = discord.Activity(name=random_status[0], type=random_status[1])
    await bot.change_presence(activity=current_active)
    await change_interval()





@bot.event
async def on_ready():
    status_changer.start()
    print(f"{bot.user.name} is ready to run!")




@bot.event
async def on_disconnect():
    status_changer.stop()



extensions=[
    'Cogs.Moderation.member',
    'Cogs.Fun.utility',
    'Cogs.Moderation.channels',
    "Cogs.Moderation.guild",
    "Cogs.Fun.music",
    'Cogs.Moderation.help',
    'Cogs.Events.background_events'
    ]



for ext in extensions:
    bot.load_extension(ext)
    print("Loaded",ext)


bot.run(os.getenv('TOKEN'),reconnect=True)