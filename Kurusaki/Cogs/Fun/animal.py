import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
import asyncio, time, requests as rq


class Animals(Cog):
    def __init__(self,bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(Animals(bot))