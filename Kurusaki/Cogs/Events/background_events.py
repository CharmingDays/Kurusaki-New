import discord,asyncio,time,random,names,requests as rq,pymongo,os
from discord.ext import commands
from discord.ext.commands import command,Cog
from discord.utils import sleep_until
import datetime


class BackgroundEvents(commands.Cog,name='Events'):
    def __init__(self,bot):
        self.bot= bot
        bot.loop.create_task(self.check_and_update())
        self.database=pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.voice=self.database.find_one("voice")


    async def check_and_update(self):
        """
        !--RUN ALL CONSISTANT BACKGROUND FUNCTIONS IN HERE--!
        """
        while True:
            currentWelcome=self.database.find_one('welcome')
            currentVoice=self.database.find_one('voice')
            if self.welcome != currentWelcome:
                self.database.update_one({'_id':'welcome'},{'$set':self.welcome})
            
            if self.voice != currentVoice:
                self.database.update_one({'_id':'voice'},{'$set':self.voice})
            
            for msg in self.temp_msg.copy():
                if time.time() >= msg:
                    try:
                        await self.temp_msg[msg].delete()
                        self.temp_msg.pop(msg)
                    except:
                        self.temp_msg.pop(msg)
                        #Message already deleted?

            await asyncio.sleep(750)



    @Cog.listener('on_voice_state_update')
    async def voice_passive_income(self,user,before,after):
        """
        Keeps track of how long users have been in a voice call
        """
        if user.bot == True:
            #Don't track bots
            return
        
        if str(user.id) not in self.voice:
            self.voice[str(user.id)]=0

        if after.channel is not None:
            #User joins voice
            if str(user.id) in self.voice:
                self.local_voice_timer[user.id]=time.time()


        if after.channel is None:
            #User leaves voice channel
            if user.id in self.local_voice_timer and str(user.id) in self.voice:
                self.voice[str(user.id)]+=int(time.time()-self.local_voice_timer[user.id])
                self.local_voice_timer.pop(user.id)


    @Cog.listener('on_command')
    async def cmd_counter(self,msg):
        if msg.author.id == 185181025104560128 and msg.command.is_on_cooldown == True:
            msg.command.reset_cooldown(msg)




    @Cog.listener('on_reaction_add')
    async def reaction_message_remove(self,emoji,user):
        if user.id != self.bot.user.id:
            if emoji.message.guild is not None and user.guild_permissions.manage_messages is True and emoji.message.author.id == self.bot.user.id:
                return await emoji.message.delete()
            if emoji.message.guild is None and emoji.message.author.id == self.bot.user.id:
                return await emoji.message.delete()



    @Cog.listener('on_message')
    async def message_tracker(self,msg):
        if msg.author.id == self.bot.user.id:
            await msg.add_reaction(emoji='❌')

        if msg.author.bot is True:
            return
        

        if msg.channel.type != discord.TextChannel:
            return None

        

    @commands.Cog.listener('on_command_error')
    async def all_command_error(self,msg,error):
        if self.error_chan is None:
            self.error_chan=self.bot.get_channel(self.error_log)

        #TODO: Attempt to make a correction suggestion here using `re` lib
        if isinstance(error,commands.CommandOnCooldown):
            return await msg.send(f"Command is on cooldown, please try again in {round(error.cooldown.retry_after,2)} seconds")
        
        if isinstance(error,commands.MissingRequiredArgument):
            pass
            #TODO:Command argument is missing with the value parm
    
        if isinstance(error,commands.BadArgument):
            #TODO: add a fix for this error
            pass

        if isinstance(error,commands.CommandError):
            if '60003' in error.args[0]:
                return await msg.send("Two factor is enabled for the server, please disable it temporarily to use the command")
    
            print(error)

        if isinstance(error,commands.PrivateMessageOnly):
            return await msg.send("This command can only be used inside a private message (PM/DM)")

        if isinstance(error,commands.NoPrivateMessage):
            return await msg.send("Command unable to run inside a private message (PM/DM")

        if isinstance(error,commands.CheckAnyFailure):
            #TODO: add a fix for this error
            pass

        if isinstance(error,commands.CommandNotFound) and msg.guild.id != 264445053596991498:
            content=msg.message.content.replace(f"{msg.prefix}","")
            return await msg.send(f"Command {content} is not found")

        if isinstance(error,commands.DisabledCommand):
            return await msg.send(f"Command {msg.command.name} is disabled")

        if isinstance(error,commands.TooManyArguments):
            return await msg.send("Too many values were used for the command")
        
        if isinstance(error,commands.CommandOnCooldown):
            pass
            #TODO: Add a fix for this error
            # return await msg.send(f"Command is on cooldow for another {msg} seconds")

        if isinstance(error,commands.NotOwner):
            return await msg.send("This command is only for the bot owners")

        if isinstance(error,commands.MissingPermissions):
            #TODO: Add a fix for this error
            pass


        if isinstance(error,commands.BotMissingPermissions):
            #TODO: Add a fix for this error
            pass
        print(error)




    @command()
    async def voice(self,msg,user:discord.Member=None):
        """
        Shows how long your or mentioned user has stayed in a voice channel
        `Ex:` .voice
        `Ex:` .voice @User1
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
        Shows the top 10 tanks
        `Ex:` .voice-rank
        `Ex:` .voice-rank 20
        `Note:` Limit is 60
        """
        if pages > 60:
            pages=60
            await msg.send("Pages can't exceed 60",delete_after=60)
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
