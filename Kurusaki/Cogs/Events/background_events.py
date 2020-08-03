import discord,asyncio,time,random,names,requests as rq,pymongo,os,json
from discord.ext import commands
from discord.ext.commands import command
from discord.utils import sleep_until
import datetime
from discord.ext import tasks

class BackgroundEvents(commands.Cog,name='Events'):

    def __init__(self,bot):
        self.bot= bot
        self.database=pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.voice=self.database.find_one("voice")
        self.member_join=self.database.find_one("member_join")
        self.michelley=287369884940238849
        self.cultivators="s5mXMXV"
        self.youtube_viewers='35WqJ7d'
        self.invite_uses={
            'cult':0,
            'youtube':0
        }
        # self.background_looper.start()
        bot.loop.create_task(self.background_functions())


    async def chat_bot(self,query):
        """
        Request query to the api.ai for chat bot
        """
        TOKEN="ad1c55f60a78435195cd95fc4bba02e9"
        BASE_URL=f"https://api.dialogflow.com/v1/query?v=20150910&sessionId=12345&lang=en&query={query}"
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        r=rq.get(url=BASE_URL,headers=headers)
        return r


    def cog_unload(self):
        current=self.database.find_one('voice')
        if current != self.voice:
            self.database.update_one({'_id':'voice'},{'$set':self.voice})




    async def background_functions(self):
        self.bot.loop.create_task(self.check_and_update())


    async def check_and_update(self):
        """
        !--RUN ALL CONSISTANT BACKGROUND FUNCTIONS IN HERE--!
        """
        while True:
            current_voice=self.database.find_one('voice')
            
            if self.voice != current_voice:
                self.database.update_one({'_id':'voice'},{'$set':self.voice})
            
            await asyncio.sleep(750)


    @commands.Cog.listener('on_voice_state_update')
    async def voice_passive_income(self,user,before,after):
        """
        Keeps track of how long users have been in a voice call
        """
        pass



    @commands.Cog.listener('on_member_join')
    async def member_welcome(self,user):
        if user.guild.id in [295717368129257472]:
            code=[invite for invite in await user.guild.invites() if invite.code == self.cultivators][0]
            if code.uses > self.invite_uses['cult']:
                role=[user.guild.get_role(487097805333331979)]
                await user.edit(roles=user.roles+role)
                self.invite_uses['cult']=code.uses




    @commands.Cog.listener('on_reaction_add')
    async def reaction_message_remove(self,emote,user):
        if user.id != self.bot.user.id and user.bot is False:
    
            if emote.custom_emoji is True and emote.emoji.id == 720136533608366121: #NOTE:VALORANT
                role= [user.guild.get_role(705234981319999488)]
                if role[0] in user.roles:
                    return 
                return await user.edit(roles=user.roles+role)

            if emote.custom_emoji is True and emote.emoji.id == 720136639992561735:#NOTE:LEAGUE Public
                role=[user.guild.get_role(719780262753337394)]
                if role[0] in user.roles:
                    return 
                return await user.edit(roles=user.roles+role)

            if emote.custom_emoji is True and emote.emoji.id == 720137028448026656: #NOTE:OVERWATCH
                role=[user.guild.get_role(720174578504171581)]
                if role[0] in user.roles:
                    return 
                return await user.edit(roles=user.roles+role)



 

        

    @commands.Cog.listener('on_command_error')
    async def all_command_error(self,msg,error):
        #TODO: Attempt to make a correction suggestion here using `re` lib
        if isinstance(error,commands.CommandOnCooldown):
            return await msg.send(f"Command is on cooldown, please try again in {round(error.cooldown.retry_after,2)} seconds")

    
        if isinstance(error,commands.CommandError):
            if '60003' in error.args[0]:
                return await msg.send("Two factor is enabled for the server, please disable it temporarily to use the command")

            else:
                return error

        if isinstance(error,commands.PrivateMessageOnly):
            return await msg.send("This command can only be used inside a private message (PM/DM)")

        if error is commands.NoPrivateMessage:
            return await msg.send("Command unable to run inside a private message (PM/DM")


        if isinstance(error,commands.CommandNotFound) and msg.guild is not None and msg.guild.id != 264445053596991498:
            content=msg.message.content.replace(f"{msg.prefix}","")
            return await msg.send(f"Command {content} is not found")


        if isinstance(error,commands.NotOwner):
            return await msg.send("This command is only for the bot owners")

        print(error)


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
    @command(name='inc-voice',aliases=['add-voice'],hidden=True)
    async def inc_voice(self,msg,user:discord.Member,amt:int=900):
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
    bot.add_cog(BackgroundEvents(bot))