import discord
from discord.ext import commands
import random

bot=commands.Bot(command_prefix='....!@#')

@bot.event
async def on_ready():
    chan=bot.get_channel(720205395016286225)
    await chan.send(file=discord.File(fp=r'Cogs\Events\error_logs.json',filename=f'Error_Logs{random.uniform(1,10)}.json'))
    await bot.logout()


bot.run('NDA1OTA3MzI2MDUxMDI0OTA2.XjJdZA.7EBDDEZ-SIX0FofndFy2Kfv9rBs')