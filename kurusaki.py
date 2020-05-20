import discord,asyncio
from discord.ext import commands



def get_prefix(bot, msg):

    prefixes = ['s.', 'a.','!']


    return commands.when_mentioned_or(*prefixes)(bot, msg)

bot = commands.Bot(command_prefix=get_prefix,description='Discord multiple command prefix')

@bot.event
async def on_ready():
    print(bot.user.name)


bot.run('NDA1OTA3MzI2MDUxMDI0OTA2.XjJdZA.7EBDDEZ-SIX0FofndFy2Kfv9rBs')
