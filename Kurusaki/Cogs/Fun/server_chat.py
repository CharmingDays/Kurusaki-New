import asyncio,time,datetime,random,names,pymongo,discord,os
from discord.ext import commands
from discord.ext.commands import Cog, command



class ServerChat(commands.Cog):
    def __init__(self,bot):
        self.bot=bot



def setup(bot):
    bot.add_cog(ServerChat(bot))
