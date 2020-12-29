import discord,asyncio
from discord.ext.commands.converter import CategoryChannelConverter
from discord.ext import commands
from discord.ext.commands import Cog,command
import pymongo,typing,json
import os,time,datetime,random



#TODO: CREATE CUSTOM SERVER ECON FOR PREMIUM
class Economy(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.econ_setup()




    def econ_setup(self):
        pass



    @Cog.listener('on_message')
    async def economyMesage(self,msg):
        self.calEcon(msg)


def setup(bot):
    bot.add_cog(Economy(bot))