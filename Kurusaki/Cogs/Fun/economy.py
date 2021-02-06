import discord,asyncio
from discord.ext.commands.converter import CategoryChannelConverter
from discord.ext import commands
from discord.ext.commands import Cog,command
import pymongo,typing,json
import os,time,datetime,random



#TODO: CREATE CUSTOM SERVER ECON FOR PREMIUM




class Rewards(object):
    """
    Server:
        increase bot prefixes
        custom econ system
        music bot playlist
    User:
        virtual items
        Role purchase 
        color purchase

        Change bot status


    """








class Economy(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.econ_setup()




    def econ_setup(self):
        """
        Setup database connection to MongoDB
        Data structure --> {"User":points:int}
        """
        #TODO: local_database
        setattr(self,'client',pymongo.MongoClient(os.getenv('MONGO')))
        setattr(self,'collection',self.client['Discord-Bot-Database']['General'])
        doc = self.collection.find_one({'_id':'gen_econ'})
        setattr(self,'econ',doc)
        self.client.close()



    @Cog.listener('on_message')
    async def economyMesage(self,msg):
        pass


def setup(bot):
    bot.add_cog(Economy(bot))