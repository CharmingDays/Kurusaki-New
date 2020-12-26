import discord,asyncio
import time,datetime
from discord.ext import commands
from discord.ext.commands import command, Cog



class BotAdmin(Cog):
    def __init__(self,bot):
        self.bot= bot

    @commands.is_owner()
    @command(name='clear-cache')
    async def _clear_cache(self,msg):
        self.bot.clear()



    @commands.is_owner()
    @command(name='change-activity')
    async def _change_activity(self,msg,_type,*,activity_name):
        activity_type=None
        if _type.lower() == 'watching':
            activity_type = discord.ActivityType.watching

        if _type.lower() == 'listening':
            activity_type = discord.ActivityType.listening

        if _type.lower() == 'playing':
            activity_type = discord.ActivityType.playing

        await self.bot.change_presence(name=activity_name,type=activity_type)

    @commands.is_owner()
    @command(name='change-status')
    async def _change_status(self,msg,_type):
        if _type.lower() == 'afk':
            return await self.bot.change_presence(afk=True)

        if _type.lower() == 'offline':
            return await self.bot.change_presence(status=discord.Status.offline)

        if _type.lower() == 'online':
            return await self.bot.change_presence(status=discord.Status.online)

        if _type.lower() == 'idle':
            return await self.bot.change_presence(status=discord.Status.idle)

        if _type.lower() == 'dnd':
            return await self.bot.change_presence(status=discord.Status.dnd)

        if _type.lower() == 'invisible':
            return await self.bot.change_presence(status=discord.Status.invisible)

        return await msg.send("Someting went wrong")


def setup(bot):
    bot.add_cog(BotAdmin(bot))