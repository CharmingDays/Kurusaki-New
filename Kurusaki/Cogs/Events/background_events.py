import discord,asyncio,time,random,names,requests as rq,pymongo,os
from discord.ext import commands
from discord.ext.commands import command,Cog
from discord.utils import sleep_until
import datetime


class BackgroundEvents(commands.Cog,name='Events'):
    def __init__(self,bot):
        self.bot= bot
        bot.loop.create_task(self.event_backgrounds())
        self.database=pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.welcome=self.database.find_one("welcome")
        self.voice=self.database.find_one("voice")
        self.auto_delete=self.database.find_one("auto_delete")
        self.cmd_used=self.database.find_one("cmd_used")
        self.msg_counter=self.database.find_one('message_counter')
        self.auto_roles=self.database.find_one('auto_roles')
        self.temp_msg={}
        self.counter={
            'cmd_used':0,
            'msg_counter':0
        }
        self.error_log=699565408088490045
        self.local_voice_timer={}
        self.error_chan=None
        self.tsukihi_guild=699290035953991741
        self.log_chan=699300733400645663
        self.all_aliases={}


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



    async def event_backgrounds(self):
        new_set={}
        all_aliases=[]
        for cmd in list(bot.commands):
            new_set[cmd.name]=cmd.aliases
            for aliases in cmd.aliases:
                for name in aliases:
                    if name:
                        all_aliases.append(name)
        
        new_set['all']=all_aliases

        self.all_aliases=new_set

        await self.bot.wait_until_ready()
        self.bot.loop.create_task(self.check_and_update())


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


        if msg.guild is not None and str(msg.guild.id) in self.cmd_used:
            self.cmd_used[str(msg.guild.id)]+=1
            self.counter['cmd_used']+=1
            if self.counter['cmd_used'] >= 100:
                self.counter['cmd_used']=0
                self.database.update_one({'_id':'cmd_used'},{'$set':self.cmd_used})

        if msg.guild is not None and str(msg.guild.id) not in self.cmd_used:
            self.cmd_used[str(msg.guild.id)]=1
            self.counter['cmd_used']+=1



    @Cog.listener('on_reaction_add')
    async def reaction_message_remove(self,emoji,user):
        if user.id != self.bot.user.id:
            if emoji.message.guild is not None and user.guild_permissions.manage_messages is True and emoji.message.author.id == self.bot.user.id:
                return await emoji.message.delete()
            if emoji.message.guild is None and emoji.message.author.id == self.bot.user.id:
                return await emoji.message.delete()

    @Cog.listener('on_message')
    async def message_tracker(self,msg):
        if msg.author.bot is True:
            return

        

        if msg.author.id == self.bot.user.id:
            await msg.add_reaction(emoji='❌')


        if msg.channel.type != discord.TextChannel:
            return None

        if msg.author.id == self.bot.user.id and str(msg.guild.id) in self.auto_delete:
            self.temp_msg[time.time()+self.auto_delete[str(msg.guild.id)]]=msg 


        if msg.author.bot == False:
            if self.counter['msg_counter'] >= 350:
                #Update database
                self.counter['msg_counter']=0
                self.database.update_one({'_id':'msg_counter'},{'$set':self.msg_counter})


            if str(msg.author.id) in self.msg_counter:
                if msg.guild.id not in self.msg_counter[str(msg.author.id)]['servers']:
                    self.msg_counter[str(msg.author.id)]['servers'].append(msg.guild.id)

                self.msg_counter[str(msg.author.id)]['msgs']+=1
                self.msg_counter[str(msg.author.id)]['length']+=len(msg.content)
                self.counter['msg_counter']+=1

            if str(msg.author.id) not in self.msg_counter:
                self.msg_counter[str(msg.author.id)]={
                    "msgs":1,
                    "servers":[msg.guild.id],
                    "length":len(msg.content)
                }
                self.counter['msg_counter']+=3
        
        

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
        


    @Cog.listener('on_guild_join')
    async def on_guild_join_greet(self,guild):
        log = self.bot.get_channel(self.log_chan)
        embed = discord.Embed(colour=0x62f442, description=f"Tsukihi has joined `{guild.name}`! Tsukihi is now in `{str(len(self.bot.guilds))}` guilds!")
        online = len([x for x in guild.members if x.status == discord.Status.online])
        idle = len([x for x in guild.members if x.status == discord.Status.idle])
        dnd = len([x for x in guild.members if x.status == discord.Status.dnd])
        offline = len([x for x in guild.members if x.status == discord.Status.offline])
        embed.add_field(name=f"Members ({len(guild.members)}):", value=f"<:online:699364552403582996> {online} <:idle:699364394324197512> {idle} <:dnd:699364348803547197> {dnd} <:invis:699364442235731978> {offline}")
        embed.set_footer(text=f'ID: {guild.id}', icon_url=guild.icon_url_as(format='png'))
        await log.send(embed=embed)
        server = guild
        targets = [
                discord.utils.get(guild.channels, name="bot"),
                discord.utils.get(guild.channels, name="bots"),
                discord.utils.get(guild.channels, name="bot-commands"),
                discord.utils.get(guild.channels, name="bot-spam"),
                discord.utils.get(guild.channels, name="bot-channel"),
                discord.utils.get(guild.channels, name="testing"),
                discord.utils.get(guild.channels, name="testing-1"),
                discord.utils.get(guild.channels, name="general"),
                discord.utils.get(guild.channels, name="shitposts"),
                discord.utils.get(guild.channels, name="off-topic"),
                discord.utils.get(guild.channels, name="media"),
                guild.get_member(guild.owner.id)
                ]
        embed = discord.Embed(colour=0x419400, title="Thanks for inviting me to your server!", description="Here is some useful information:")
        embed.add_field(name="Getting Started", value="You can use `.help` to get a list of modules, information on a command.", inline=True)
        embed.add_field(name="Need help?", value="Have suggestions/bugs reports or just need help? join our [server](https://discord.gg/SUkhU4n)", inline=True)
        embed.set_thumbnail(url=guild.icon_url_as(format='png'))
        for x in targets:
            try:
                return await x.send(embed=embed) #Breaks loop
            except:
                continue


    @Cog.listener('on_guild_remove')
    async def on_guild_remove_cog(self,guild):
        log = self.bot.get_channel(self.log_chan)
        embed = discord.Embed(colour=0xf44141, description=f"Tsukihi has been kicked from `{guild.name}`.. Tsukihi is now in `{str(len(self.bot.guilds))}` guilds.")
        embed.set_footer(text=f'ID: {guild.id}', icon_url=guild.icon_url_as(format='png'))
        return await log.send(embed=embed)


    @Cog.listener('on_member_join')
    async def event_member_join(self,member):
        if str(member.guild.id) in self.auto_roles:
            roles=[]
            for role in self.auto_roles[str(member.guild.id)]:
                try:
                    Role=member.guild.get_role(role)
                    roles.append(Role)

                except:
                    self.auto_roles[str(member.guild.id)].remove(role)
                    if not self.auto_roles[str(member.guild.id)]:
                        self.auto_roles.pop(str(member.guild.id))

            return await member.edit(roles=member.roles+roles)


        if member.guild.id == self.tsukihi_guild:
            log = self.bot.get_channel(699301852013002862)
            mutual = "`, `".join([x.name for x in self.bot.guilds if member in x.members])
            embed = discord.Embed(colour=0x419400, description=f"Welcome to **Tsukihi Hideout**, {member.mention}! For support, use <#699302666358095913> and our <@&699297490989482194> is ready to help!\n\n**Mutual Guilds**: `{mutual}`")
            embed.set_thumbnail(url=member.avatar_url_as(format='png'))
            embed.set_footer(text="Member Join", icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await log.send(embed=embed)
            await member.send("Welcome to **Tsukihi's Hideout**, Please review the rules & info in <#699349510719012956> and <#699301258531438612> for support, use <#699302666358095913> and our the Support Team is ready to help!")
    



    @commands.Cog.listener('on_member_remove')
    async def event_on_member_remove(self, member):
        if member.guild.id == self.tsukihi_guild:
            quotes = ['So long, farewell, auf Wiedersehen, goodbye. I leave and heave a sigh and say goodbye.', 'Hasta la vista, baby', 'Good luck, we\'re all counting on you', 'You have been my friend. That in itself is a tremendous thing.', 'Never say goodbye because goodbye means going away and going away means forgetting', 'I make it easier for people to leave by making them hate me a little.', 'Agh.. finally.']
            log = self.bot.get_channel(699301852013002862)
            embed = discord.Embed(colour=0xf44141, description=f"Goodbye, **{member}**! {random.choice(quotes)}")
            embed.set_thumbnail(url=member.avatar_url_as(format='png'))
            embed.set_footer(text="Member Leave", icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await log.send(embed=embed)
        


    @command(hidden=True,enabled=False)
    async def autorole(self,msg,*roles:discord.Role):
        if not roles:
            return await msg.send("Please mention the role(s) to auto add for when members join")
        
        if roles:
            role_ids=[role.id for role in roles]
            if str(msg.guild.id) in self.auto_roles:
                self.auto_roles[str(msg.guild.id)]+role_ids
            

            if str(msg.guild.id) not in self.auto_roles:
                self.auto_roles[str(msg.guild.id)]=role_ids

            return await msg.send(f"Added role(s) {' '.join([role.name for role in roles])} to auto roles")




    @command(name='msg-counter',hidden=True)
    async def msg_counter(self,msg,user:discord.Member=None):
        if user is None:
            if str(msg.author.id) in self.msg_counter:
                return await msg.send(f"`{self.msg_counter[str(msg.author.id)]['msgs']}` tracked with `{self.msg_counter[str(msg.author.id)]['length']}` length")

        if user is not None:
            if str(user.id) in self.msg_counter:
                return await msg.send(f"`{self.msg_counter[str(user.id)]['msgs']}` messages tracked with `{self.msg_counter[str(user.id)]['length']}` length")



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
            return await msg.send("Somethin gwent wrong")





def setup(bot):
    bot.add_cog(BackgroundEvents(bot))
