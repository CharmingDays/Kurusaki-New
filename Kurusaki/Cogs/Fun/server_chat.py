import asyncio,time,datetime,random,names,pymongo,discord,os
from discord.ext import commands
from discord.ext.commands import Cog, command



class ServerChat(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.database = pymongo.MongoClient(os.getenv['MONGO'])['Discord-Bot-Database']['General']
        self.channels={} #{channel id: web obj}
        self.chat_guilds=[] #All in ID form
        self.blacklist=self.database.find_one('chat_blacklist') #list connencting to database later after the complete user id
        self.counter={}
        self.chat_name='tsukihi_chat_channel'
        self.temp_mute={}
        self.temp_mute_server={}


    async def update_black_list(self,user):
        self.blacklist.append(str(user))
        self.database.update_one({'_id':'chat_blacklist'},{'$set':self.blacklist})



    async def chat_start_check(self):
        """
        Add all the guilds with the text channel into the self.chat_guilds list
        """
        for chan in self.bot.get_all_channels():
            if isinstance(chan,discord.TextChannel) and chan.name.lower() == self.chat_name and chan.guild.id not in self.chat_guilds:
                hooks=await chan.webhooks()
                self.chat_guilds.append(chan.guild.id)
                if hooks:
                    self.channels[chan.id]=hooks[0]
                else:
                    hook=await chan.create_webhook(name=self.chat_name)
                    self.channels[chan.id]=hook

    async def clear_temp_mute(self):
        while True:
            if self.temp_mute:
                for i in self.temp_mute.copy():
                    if time.time() >=self.temp_mute[i]:
                        self.temp_mute.pop(i)
            await asyncio.sleep(10)


    @commands.Cog.listener('on_ready')
    async def chat_server_ready(self):
        await self.chat_start_check()
        clear_temp_loop=asyncio.wait([self.clear_temp_mute()])
        await clear_temp_loop




    @commands.Cog.listener('on_guild_channel_create')
    async def chat_create(self,channel):
        if channel.name.lower() == self.chat_name and channel.guild.id not in self.chat_guilds: #Check only 1 channel exist
            self.chat_guilds.append(channel.guild.id)
            hook=await channel.create_webhook(name=names.get_first_name())
            self.channels[channel.id]=hook
        


    @commands.Cog.listener('on_guild_channel_delete')
    async def chat_delete(self,channel):
        if channel.name.lower() == self.chat_name and channel.guild.id in self.chat_guilds:
            self.chat_guilds.remove(channel.guild.id)
            del self.channels[channel.id]



    @commands.Cog.listener('on_message')
    async def chat_message(self,msg):
        """
        An on_message event reference used for allowing multiple servers to communicate with each other through having a text channel called `kurusaki_server_chat`
        Only one will be avaliable per server.
        Features
            - Channel includes auto slow mode of `5` seconds 
            - Spam detect mode from users with higher perms and other means of spam
            - Auto mute function for the spammers
            - Blacklist function and auto un-mute function
        """
        if msg.channel.name.lower() == self.chat_name and msg.author.bot is False and str(msg.author.id) not in self.blacklist and msg.author.id not in self.temp_mute and msg.author.id not in self.temp_mute_server:
            for channel in self.channels:
                if channel != msg.channel.id:
                    #Send format with webhook in embed format to include user id if possible
                    emb=discord.Embed(description=msg.content)
                    emb.set_footer(text=msg.author.id,icon_url=msg.guild.icon_url)
                    await self.channels[channel].send(embed=emb,username=msg.author.name,avatar_url=msg.author.avatar_url)


            if msg.author.id in self.counter:
                if self.counter[msg.author.id]['hits'] >=3:
                    self.temp_mute[msg.author.id]=time.time()+900
                    report=self.bot.get_channel(682513406682857540)
                    await report.send(f"{msg.author.name}: ({msg.author.id}) temp muted")
                    try:
                        return await msg.author.send("You have been temporarily muted for 15 minnute from auto anti-spam detector\nRepeated spam will result in being blacklist")
                    except (commands.CommandInvokeError,discord.errors.Forbidden):
                        return await msg.channel.send(f"{msg.author.mention}, you have been temporarily muted for 15 minutes from auto anti-spam detector\nRepeated spam will result in being blacklist")


                if time.time() < self.counter[msg.author.id]['time']:
                    self.counter[msg.author.id]['time']+5
                    if len(msg.content) >= 500:
                        self.counter[msg.author.id]['hits']+=3
                    self.counter[msg.author.id]['hits']+=1
                
            else:
                if msg.author.id not in self.counter:
                    self.counter[msg.author.id]={'time':time.time()+5,'hits':0}


   

    @commands.is_owner()
    @commands.command(name='chat-blacklist')
    async def chat_blacklist(self,msg,user:int): #The discord user's ID
        await self.update_black_list(user)



    @command(name='report-chat',aliases=['reportchat','report_chat'])
    async def report_chat(self,msg,user_id:int,*,reason=None):
        if reason is not None:
            me = self.bot.get_channel(682482921541730442)
            return await me.send(f"Reporter: {msg.author.name} ({msg.author.id})\nReported: {user_id}\nReason: {reason}")
        return await msg.send("Please provide a reason for reporting the user")


    @report_chat.error
    async def report_chat_error(self,msg,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await msg.send("please enter the user's ID  you're reporting")


    def server_owner():
        # pylint: disable=no-method-argument
        def predicate(msg):
            return msg.author.id == msg.guild.owner_id
        return commands.check(predicate)


    @server_owner()
    @command(name='temp-mute')
    async def _temp_mute(self,msg,*users:discord.Member):
        message=""
        if users:
            for i in users:
                self.temp_mute_server[i.id]=time.time()+900
                message+=f"{i.mention} "
            await msg.send(f"{message} have been temporarily server muted for 15 minutes")

        return await msg.send("Please mention your server member(s) to mute")
        


    @_temp_mute.error
    async def temp_mute_error(self,msg,error):
        if isinstance(error,commands.CheckFailure):
            await msg.send("Only server owners can use this command")
            


    @server_owner()
    @command()
    async def remove_temp_mute(self,msg,*users:discord.Member):
        message=""
        if users:
            for i in users:
                self.temp_mute_server.pop(msg.author.id)
                message+=f"{i.mention} "
            await msg.send(f"{message} have been removed from server mute")

        return await msg.send("Please mention your server member(s) to mute")
        



    @remove_temp_mute.error
    async def remove_temp_mute_error(self,msg,error):
        if isinstance(error,commands.CheckFailure):
            await msg.send("Only server owners can use this command")




def setup(bot):
    bot.add_cog(ServerChat(bot))
