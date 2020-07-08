import asyncio,time,datetime,random,names,pymongo,discord,os
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord.utils import sleep_until
class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @command()
    async def remind(self,msg,*,message):
        pass

    
    @command()
    async def timer(self,msg,hours,minutes,seconds):
        when=datetime.datetime.utcnow() + datetime.timedelta(hours=hours,minutes=minutes,seconds=seconds)
        timer_done=await msg.send("Timmer complete")
        sleep_until(when,timer_done)

    @command()
    async def ping(self,msg):
        return await msg.send(f"Pong! 🏓 {round(self.bot.latency,3)}")



def setup(bot):
    bot.add_cog(Utility(bot))

