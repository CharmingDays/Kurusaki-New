import discord,asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


def get_prefix(bot, msg):


    if msg.guild.id == 264445053596991498:
        return commands.when_mentioned_or(*['k.'])(bot, msg)

    prefixes = ['s.', 'k.']


    return commands.when_mentioned_or(*prefixes)(bot, msg)

bot = commands.Bot(command_prefix=get_prefix,description='A multipurpose discord bot',case_insensitive=True)



@bot.event
async def on_ready():
    current_active = discord.Activity(name='SING - Moonlight Thoughts', type=discord.ActivityType.watching)
    await bot.change_presence(activity=current_active)
    print(f"{bot.user.name} is ready to run!")






extensions=[
    'Cogs.Moderation.member',
    'Cogs.Moderation.text_channel',
    'Cogs.Moderation.help',
    "Cogs.Moderation.guild",
    'Cogs.Events.background_events'
    ]

for ext in extensions:
    bot.load_extension(ext)
    print(ext)



bot.run(os.getenv('TOKEN'))