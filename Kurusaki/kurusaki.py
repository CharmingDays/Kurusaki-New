import json
import discord,asyncio,os
from discord.ext import commands
from discord.ext.commands import Greedy
from dotenv import load_dotenv
import logging
load_dotenv()


def get_prefix(bot, msg):

    if msg.guild.id == 264445053596991498:
        return commands.when_mentioned_or(*['k.'])(bot, msg)

    prefixes = ['s.', 'k.']

    return commands.when_mentioned_or(*prefixes)(bot, msg)

bot = commands.Bot(command_prefix=get_prefix,description='A multipurpose discord bot',case_insensitive=True,owner_id=185181025104560128)



@bot.event
async def on_ready():
    current_active = discord.Activity(name='SING - Moonlight Thoughts', type=discord.ActivityType.watching)
    await bot.change_presence(activity=current_active)
    print(f"{bot.user.name} is ready to run!")



extensions=[
    'Cogs.Moderation.member',
    'Cogs.Moderation.text_channel',
    "Cogs.Moderation.guild",
    "Cogs.Fun.music",
    'Cogs.Moderation.help',
    'Cogs.Events.background_events'
    ]


for ext in extensions:
    bot.load_extension(ext)
    print(ext)



bot.run(os.getenv('TOKEN'))