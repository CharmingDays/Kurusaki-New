import discord,asyncio,time,random,names,requests as rq,pymongo,os,json
from discord.ext import commands
from discord.ext.commands import command,Cog
from discord.utils import sleep_until
import datetime
import subprocess
from discord.ext import tasks


class BackgroundEvents(commands.Cog,name='Events'):
    def __init__(self,bot):
        self.bot= bot
        bot.loop.create_task(self.check_and_update())
        self.database=pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.voice=self.database.find_one("voice")
        self.member_join=self.database.find_one("member_join")
        self.force_logout=False



    @command()
    async def logout(self,msg):
        await msg.send(os.listdir())
        self.force_logout=True
        await self.bot.logout()

    def cog_unload(self):
        if self.force_logout is True:
            subprocess.call(r"kurusaki.py",shell=True)

        else:
            subprocess.call(r"Cogs\Events\on_logout.py",shell=True)



    async def check_and_update(self):
        """
        !--RUN ALL CONSISTANT BACKGROUND FUNCTIONS IN HERE--!
        """
        while True:
            currentVoice=self.database.find_one('voice')
            
            if self.voice != currentVoice:
                self.database.update_one({'_id':'voice'},{'$set':self.voice})
            
            await asyncio.sleep(750)



    @Cog.listener('on_voice_state_update')
    async def voice_passive_income(self,user,before,after):
        """
        Keeps track of how long users have been in a voice call
        """
        pass

    @Cog.listener('on_command')
    async def cmd_counter(self,msg):
        if msg.author.id == 185181025104560128 and msg.command.is_on_cooldown == True:
            msg.command.reset_cooldown(msg)


    @Cog.listener('on_member_join')
    async def member_welcome(self,user):
        if user.guild.id == "my guild id":
            chan=self.bot.get_channel(628174714313113600)
            emojis=[self.bot.get_emoji(720136533608366121),self.bot.get_emoji(720136639992561735),self.bot.get_emoji(720137028448026656)]
            message=await chan.send("Please reaction reaction on this message to get access to the desired game channels")
            for emote in emojis:
                await message.add_reaction(emoji=emote)

        if str(user.guild.id) in self.member_join:
            chan=self.bot.get_channel(self.member_join[str(user.guild.id)]['greetings'])
            if chan is None:
                _user=self.bot.get_user(user.guild.owner_id)
                self.member_join.pop(str(user.guild.id))
                return await _user.send(f"The bot was unable to get the specifyied channel <#{self.member_join[str(user.guild.id)]['greetings']}>.\nThe bot has removed the auto new member welcomer, please reset it again.")

            if chan is not None:
                return await chan.send(f"{random.choice(self.member_join[str(user.guild.id)]['messages'])}")




    @Cog.listener('on_reaction_add')
    async def reaction_message_remove(self,emote,user):
        if user.id != self.bot.user.id:
    
            if emote.custom_emoji is True and emote.emoji.id == 720136533608366121: #NOTE:VALORANT
                role= [user.guild.get_role(705234981319999488)]
                await user.edit(roles=user.roles+role)

            if emote.custom_emoji is True and emote.emoji.id == 720136639992561735:#NOTE:LEAGUE
                role=[user.guild.get_role(719780262753337394)]
                await user.edit(roles=user.roles+role)

            if emote.custom_emoji is True and emote.emoji.id == 720137028448026656: #NOTE:OVERWATCH
                role=[user.guild.get_role(720174578504171581)]
                await user.edit(roles=user.roles+role)

            #TODO: MAKE IT SO THAT IT'S CUSTOM EMOJI SO THAT IT'S MORE SPECIFIC
            # if emote.message.guild is not None and user.guild_permissions.manage_messages is True and emote.message.author.id == self.bot.user.id:
            #     return await emote.message.delete()
            # if emote.message.guild is None and emote.message.author.id == self.bot.user.id:
            #     return await emote.message.delete()



    @Cog.listener('on_message')
    async def message_tracker(self,msg):
        #TODO: REPLACE THE X EMOJI WITH A CUSTOM "DELETE_MESSAGE" EMOJI
        # if msg.author.id == self.bot.user.id:
        #     await msg.add_reaction(emoji='❌')

        if msg.author.bot is True:
            return
        

        

    @commands.Cog.listener('on_command_error')
    async def all_command_error(self,msg,error):

        #TODO: Attempt to make a correction suggestion here using `re` lib
        if isinstance(error,commands.CommandOnCooldown):
            return await msg.send(f"Command is on cooldown, please try again in {round(error.cooldown.retry_after,2)} seconds")
        

        if isinstance(error,commands.CommandError):
            if '60003' in error.args[0]:
                return await msg.send("Two factor is enabled for the server, please disable it temporarily to use the command")
    

        if isinstance(error,commands.PrivateMessageOnly):
            return await msg.send("This command can only be used inside a private message (PM/DM)")

        if isinstance(error,commands.NoPrivateMessage):
            return await msg.send("Command unable to run inside a private message (PM/DM")


        if isinstance(error,commands.CommandNotFound) and msg.guild.id != 264445053596991498:
            content=msg.message.content.replace(f"{msg.prefix}","")
            return await msg.send(f"Command {content} is not found")


        if isinstance(error,commands.NotOwner):
            return await msg.send("This command is only for the bot owners")

        else:
            read_file=open(r'Cogs\Events\error_logs.json','r')
            data=json.loads(read_file.read())
            read_file.close()
            if str(error) not in data['logs']:
                data['logs'].append(str(error))
            file=open(r'Cogs\Events\error_logs.json','w')
            file.write(json.dumps(data))
            file.close()


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
    @command(name='voice-update')
    async def voice_update(self,msg):
        current=self.database.find_one('voice')
        if current != self.voice:
            self.database.update_one({'_id':'voice'},{'$set':self.voice})
            return await msg.message.add_reaction(emoji='✅')
        return await msg.send("No changes in database")




    @commands.is_owner()
    @command(name='inc-voice',aliases=['add-voice'])
    async def inc_voice(self,msg,user:discord.Member,amt:int):
        if str(user.id) in self.voice:
            self.voice[str(user.id)]+=amt
            return await msg.message.add_reaction(emoji='✅')
        
        else:
            self.voice[str(user.id)]=amt
            return await msg.message.add_reaction(emoji='✅')




    @commands.is_owner()
    @command(name='reset-voice-db')
    async def reset_voice_db(self,msg):
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
        except:
            return await msg.send("Something went wrong")



def setup(bot):
    bot.add_cog(BackgroundEvents(bot))