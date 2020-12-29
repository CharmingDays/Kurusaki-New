import discord,asyncio,time,random,names,requests as rq,pymongo,os,json
from discord.ext.commands.cog import Cog
from discord.ext import commands
from discord.ext.commands import command
from discord.utils import sleep_until
import datetime
from discord.ext import tasks

class Events(commands.Cog,name='Events'):

    def __init__(self,bot):
        self.bot= bot
        self.client=pymongo.MongoClient(os.getenv('MONGO'))
        self.voice_counters = {}
        self.event_setup()


    def event_setup(self):
        if hasattr(self,'voice') is False:
            data = self.client['Discord-Bot-Database']['General'].find_one({'_id':'voice'})
            data.pop('_id')
            setattr(self,'voice',data)
            self.client.close()


    def cog_unload(self):
        pass


    @Cog.listener('on_command')
    async def command_events(self,msg):
        pass #add command being used counter



    async def background_functions(self):
        self.bot.loop.create_task(self.check_and_update())


    async def check_and_update(self):
        """
        !--RUN ALL CONSISTANT BACKGROUND FUNCTIONS IN HERE--!
        """


    @commands.Cog.listener('on_voice_state_update')
    async def voice_passive_income(self,user,before,after):
        """
        Keeps track of how long users have been in a voice call
        """
        if user.bot: #NOTE: user is a bot
            return False
        if before.channel is None and after.channel is not None: #NOTE User joins voice channel
            if str(user.id) not in self.voice:
                self.voice[str(user.id)] = 0
                self.voice_counters[str(user.id)] = time.time()
            else:
                self.voice_counters[str(user.id)] = time.time()

        if before.channel is not None and after.channel is None: #NOTE User leaves voice channel
            if str(user.id) in self.voice:
                if str(user.id) in self.voice_counters:
                    #NOTE Bot missed user join
                    self.voice[str(user.id)]+= int(time.time() - self.voice_counters[str(user.id)])


                else:
                    self.voice[str(user.id)]+= 120
                try: #remove the data for space
                    self.voice_counters.pop(str(user.id))
                except KeyError:
                    #TODO: MAKE IT LOG THE ID THAT WAS NOT IN SERVER
                    pass


            else:
                self.voice[str(user.id)] = 900

            
            #UPDATE DATABASE
            self.client['Discord-Bot-Database']['General'].update_one({'_id':'voice'},{'$inc':{str(user.id):self.voice[str(user.id)]}})
            self.client.close()


        


    @command(name='voice-time')
    async def voice_time(self,msg,user:discord.Member=None):
        """
        Shows how long your or mentioned user has stayed in a voice channel
        `Ex:` .voice @User1 (If user is not mentioned, it'll send yours)
        `Command:` voice-time(user:optional)
        """
        if user is None:
            if str(msg.author.id) in self.voice:
                seconds=self.voice[str(msg.author.id)]/60
                return await msg.send(f"You have spent {round(seconds/60,4)} hours in voice channels")
            return await msg.send(f"{self.bot.user.name} has no records of your voice timer yet.")

        if user is not None:
            if str(user.id) in self.voice:
                seconds=self.voice[str(user.id)]/60
                return await msg.send(f"{user.name} has spent {round(seconds/60,4)} hours in voice channels")
            return await msg.send(f"{self.bot.user.name} has no records of **{user.name}** voice timer yet.")

    


    @commands.is_owner()
    @command(name='update-voice',hidden=True)
    async def update_voice(self,msg):
        """
        Update the database with thee current data in the memory
        """
        current=self.database.find_one('voice')
        if current != self.voice:
            self.database.update_one({'_id':'voice'},{'$set':self.voice})
            return await msg.message.add_reaction(emoji='✅')
        return await msg.send("No changes in database")




    @commands.is_owner()
    @command(name='voice-inc',aliases=['add-voice'],hidden=True)
    async def voice_inc(self,msg,user:discord.Member,amt:int=900):
        """
        Add a user to voice database with value
        """
        if str(user.id) in self.voice:
            self.voice[str(user.id)]+=amt
            return await msg.message.add_reaction(emoji='✅')
        
        else:
            self.voice[str(user.id)]=amt
            return await msg.message.add_reaction(emoji='✅')




    @commands.is_owner()
    @command(name='reset-voice-db',hidden=True)
    async def reset_voice_db(self,msg):
        """
        Replace the current local data with the cloud
        """
        current=self.database.find_one('voice')
        if self.voice != current:
            self.voice=current.copy()
            return await msg.message.add_reaction(emoji='✅')

        return await msg.send("No new changes in database detected")



    @command(name='voice-rank',aliases=['voiceRank'])
    async def voice_rank(self,msg,pages=10):
        """
        Shows the top 10 ranks
        `Ex:` .voice-rank
        `Ex:` .voice-rank 20
        `Note:` Limit is 60
        """
        if pages > 60:
            pages=60
            await msg.send("Pages can't exceed 60")
            await asyncio.sleep(1)
        new_voice=self.voice.copy()
        new_voice.pop('_id')
        ranks=""
        user_dict={}

        for user in self.bot.get_all_members():
            if str(user.id) in self.voice:
                user_dict[user.id]=user.name

        for user in self.voice.copy():
            if user != '_id' and int(user) not in user_dict:
                try:
                    self.voice.pop(user)
                except KeyError:
                    if self.error_chan is None:
                        self.error_chan=self.bot.get_channel(self.error_log)
                    await self.error_chan.send(f"Could not remove {user}")


        for index,user in enumerate(sorted(new_voice.items(),key=lambda x: x[1],reverse=True)):
            if index+1 > pages:
                break

            else:
                
                ranks+=f"{index+1}: {user_dict[int(user[0])]} - {round(((user[1]/60)/60),4)} hours\n"
        
        try:
            return await msg.send(f"```yaml\n{ranks}```")
        except Exception:
            return await msg.send("Something went wrong.\nPlease try again later")



def setup(bot):
    bot.add_cog(Events(bot))