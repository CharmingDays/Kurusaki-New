import asyncio,time,datetime,random,names,pymongo,discord,os
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord.utils import sleep_until
class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    async def timer_completed(self,msg):
        await msg.send(f"Timer complete, {msg.author.mention}")

    @commands.cooldown(rate=2,per=30,type=commands.BucketType.user)
    @command(name='set-timer')
    async def set_timer(self,msg,hours,minutes,seconds):
        """
        Set a timer to do for the bot
        `Ex`: s.set-timer 2 31 23
        `Format`: Hours Minutes Seconds
        `Cooldown`: 30 seconds per command per user
        `Command`: set-timer(hours,minutes,seconds)
        """
        when=datetime.datetime.utcnow() + datetime.timedelta(hours=hours,minutes=minutes,seconds=seconds)
        timer=sleep_until(when,self.timer_completed)
        return await timer(msg)



    @command(aliases=['latency'])
    async def ping(self,msg):
        """
        Check to see how long it's taking for the bot to respond to you
        """
        return await msg.send(f"Pong! 🏓 {round(self.bot.latency,3)}")



def setup(bot):
    bot.add_cog(Utility(bot))

