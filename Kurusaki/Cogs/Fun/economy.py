import discord,asyncio
from discord.ext.commands.converter import CategoryChannelConverter
from discord.ext import commands
from discord.ext.commands import Cog,command
import pymongo,typing,json
import os,time,datetime,random

class Economy(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.econTasks={}
        self.attemptConnection()
        # bot.loop.create_task(self.background_events())




    def startFunctions(self):
        pass


    def attemptConnection(self):
        databaseURI = os.getenv('MongoURI')
        if databaseURI is None:
            setattr(self,'database',dict(name='_id',value='economyId'))
            return 204

        if databaseURI is not None:
            try:
                client = pymongo.MongoClient(databaseURI,connect=True)
                client['discordBot']['economy']
                document = client.find_one('economyId')
                if document is None:
                    document = dict(name='_id',value='economyId')

                client.insert_one(document)
                setattr(self,'database',document)
            except:
                setattr(self,'database',dict(name='_id',value='economyId'))


    def calEcon(self,msg):
        coin = len(msg.message) / 5

        self.database[str(msg.author.id)] ={"coins":coin}


    @Cog.listener('on_message')
    async def economyMesage(self,msg):
        self.calEcon(msg)


def setup(bot):
    bot.add_cog(Economy(bot))