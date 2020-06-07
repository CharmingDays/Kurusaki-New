import asyncio,time,datetime,random,names,pymongo,discord,os
from discord.ext import commands
from discord.ext.commands import Cog, command


class ServerChat(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.channel_name='kurusaki_channel'
        self.duplicate_channel=[]
    

    async def check_duplicate_channels(self):
        while True:
            guilds=[]
            for chan in self.bot.get_all_channels():
                if chan.guild.id not in guilds:
                    guilds.append
                
                else:
                    if chan.id not in self.duplicate_channel:
                        self.duplicate_channel.append(chan.id)
            
            await asyncio.sleep(1500)


    async def kurusaki_channel_webhooks(self):
        for chan in self.bot.get_all_channels():
            if chan.name == self.channel_name:
                if not await chan.webhooks():
                    await chan.create_webhook(name=self.channel_name,reason='Webhook created for kurusaki server chat')




    @Cog.listener('on_message')
    async def server_chat_message(self,msg):
        if msg.channel.name == self.channel_name:
            for chan in self.bot.get_all_channels():
                if chan.id not in self.duplicate_channel:
                    await chan.webhooks()[0].send(content=msg.message.content,avatar_url=msg.author.avatar_url)


    @command()
    async def server_chat(self,msg,mode):
        if mode.lower() == 'off':
            for chan in msg.guild.text_channels:
                if chan.name == self.channel_name:
                    await chan.delete()
                    return await msg.send(f"Turned off server chat for `{msg.guild.name}`")
            return await msg.send(f"No server chat channel found inside P{msg.guild.name}")

        if mode.lower() == 'on':
            for chan in msg.guild.text_channels:
                if chan.name == self.channel_name:
                    return await msg.send(f"Server chat channel already exist for {msg.guild.name}")
            return await msg.guild.create_text_channel(name=self.channel_name,slowmode_delay=40,reason="Channel created for kurusaki bot's server chat")






def setup(bot):
    bot.add_cog(ServerChat(bot))