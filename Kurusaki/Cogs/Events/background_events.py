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
        self.days={"morning":False,"afternoon":False,"evening":False,"night":False,"day":datetime.datetime.now().day}
        self.jia_greetings={"morning":["Good morning, Yukinno"],"afternoon":["Good afternoon, Yukinno"],"evening":["Good evening, Yukinno"],"night":["Good night, Yukinno 💤"]}
        self.member_join=self.database.find_one("member_join")
        self.michelley=287369884940238849
        self.special_invite="XVTex62"
        self.invite_uses=0
        self.jia_yi.start()
        bot.loop.create_task(self.background_functions())


    @staticmethod
    async def chat_bot(query):
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


    #NOTE:Something to do when the bot disconnects; will not have access to the discord API anymore
    def cog_unload(self):
        self.jia_yi.cancel()


    @tasks.loop(hours=1)
    async def jia_yi(self):
        #NOTE: wait until bot is ready for cache
        await self.bot.wait_until_ready()
        now=datetime.datetime.utcnow() - datetime.timedelta(hours=4)
        if self.days['day'] < now.day:
            self.days['day'] = now.day

        if now.hour in [7,8,9,10,11] and self.days['morning'] is False:
            user=self.bot.get_user(self.michelley)
            self.days['morning']=True
            self.days['night']=False
            await user.send(random.choice(self.jia_greetings['morning']))

        if now.hour in [12,13,14,15,16] and self.days['afternoon'] is False:
            user=self.bot.get_user(self.michelley)
            await user.send(random.choice(self.jia_greetings['afternoon']))
            self.days['afternoon']=True
            self.days['morning']=False

        if now.hour in [17,18,19,20] and self.days['evening']:
            user=self.bot.get_user(self.michelley)
            await user.send(random.choice(self.jia_greetings['evening']))
            self.days['evening']=True
            self.days['afternoon']=False

        if now.hour in [22,23,24] and self.days['night'] is False:
            user=self.bot.get_user(self.michelley)
            await user.send(random.choice(self.jia_greetings['night']))
            self.days['night']=True
            self.days['evening']=False

    async def background_functions(self):
        self.bot.loop.create_task(self.check_and_update())


    async def check_and_update(self):
        """
        !--RUN ALL CONSISTANT BACKGROUND FUNCTIONS IN HERE--!
        """
        while True:
            currentVoice=self.database.find_one('voice')
            
            if self.voice != currentVoice:
                self.database.update_one({'_id':'voice'},{'$set':self.voice})
            
            await asyncio.sleep(750)


    @commands.Cog.listener('on_voice_state_update')
    async def voice_passive_income(self,user,before,after):
        """
        Keeps track of how long users have been in a voice call
        """
        pass

    # @commands.Cog.listener('on_command')
    # async def cmd_counter(self,msg):
    #     pass


    @commands.Cog.listener('on_member_join')
    async def member_welcome(self,user):
        if user.guild.id in [295717368129257472]:
            code=[invite for invite in await user.guild.invites() if invite.code == self.special_invite][0]
            if code.uses > self.invite_uses:
                role=[user.guild.get_role(578750959367225375)]
                await user.edit(roles=user.roles+role)
                self.invite_uses=code.uses
            # chan=self.bot.get_channel(628174714313113600) #NOTE: Disboard channel
            # emojis=[self.bot.get_emoji(720136533608366121),self.bot.get_emoji(720136639992561735),self.bot.get_emoji(720137028448026656)]
            # message=await chan.send(f"{user.mention} Please reaction reaction on this message to get access to the desired game channels")
            # for emote in emojis:
            #     await message.add_reaction(emoji=emote)

        if str(user.guild.id) in self.member_join:
            chan=self.bot.get_channel(self.member_join[str(user.guild.id)]['greetings'])
            if chan is None:
                _user=self.bot.get_user(user.guild.owner_id)
                self.member_join.pop(str(user.guild.id))
                return await _user.send(f"The bot was unable to get the specifyied channel <#{self.member_join[str(user.guild.id)]['greetings']}>.\nThe bot has removed the auto new member welcomer, please reset it again.")

            if chan is not None:
                return await chan.send(f"{random.choice(self.member_join[str(user.guild.id)]['messages'])}")



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






    @commands.Cog.listener('on_message')
    async def message_tracker(self,msg):
        if not isinstance(msg.channel,discord.TextChannel):
            return None

        if msg.author.bot is True:
            return None

        if msg.guild.id in [251397504879296522,295717368129257472]:
            if f"<@!{self.bot.user.id}>" in msg.content:
                content=msg.content.replace('<@!403402614454353941> ','')
                data=await self.chat_bot(content)
                if data.ok:
                    reply=data.json()['result']['fulfillment']['speech']
                    if reply == '#love':
                        not_yukinno=[f"Sorry {msg.author.name}, but I'm already taken by someone","I'm already taken \:)",f"Sorry, I'm already taken {msg.author.name}"]
                        is_yukinno=['❤','<3','I ❤ you',f'I love you {msg.author.display_name}',f'My love is only for you {msg.author.name}']
                        if msg.author.id == 287369884940238849:
                            return await msg.channel.send(random.choice(is_yukinno))
                        else:
                            return await msg.channel.send(random.choice(not_yukinno))

                    return await msg.channel.send(reply)
                if not data.ok:
                    return await msg.channel.send("Sorry, I'm experiencing some technical issues, please try again later D:")
                    

        

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

        if isinstance(error,commands.NoPrivateMessage):
            return await msg.send("Command unable to run inside a private message (PM/DM")


        if isinstance(error,commands.CommandNotFound) and msg.guild.id != 264445053596991498:
            if msg.guild.id == 295717368129257472:
                return None
            content=msg.message.content.replace(f"{msg.prefix}","")
            return await msg.send(f"Command {content} is not found")


        if isinstance(error,commands.NotOwner):
            return await msg.send("This command is only for the bot owners")

        return error


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
    @command(name='update-voice')
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
    @command(name='inc-voice',aliases=['add-voice'])
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
    @command(name='reset-voice-db')
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
        except Exception as Error:
            return await msg.send("Something went wrong.\nPlease try again later")



def setup(bot):
    bot.add_cog(BackgroundEvents(bot))