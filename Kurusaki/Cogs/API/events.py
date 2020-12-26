from discord.ext import commands
from discord.ext.commands import Cog,command
from discord.ext import tasks
import discord, asyncio, time
import os, random, typing


class Events(Cog):
    def __init__(self,client):
        self.bot = client



def setup(bot):
    bot.add_cog(Events(bot))
