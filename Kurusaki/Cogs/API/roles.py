import discord,asyncio,time,datetime,random,requests as rq
from discord.ext import commands
from discord.ext.commands import Cog,command
from discord.utils import sleep_until

current_time=datetime.datetime.now()
date=datetime.datetime(year=current_time.year,month=current_time.month,day=current_time.day,hour=current_time.hour,minute=current_time.minute,second=current_time.second+5)





class Roles(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.role_emote_perms=[]






def setup(bot):
    bot.add_cog(Roles(bot))