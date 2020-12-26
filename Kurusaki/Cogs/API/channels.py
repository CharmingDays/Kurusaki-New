from typing import Optional
import discord,asyncio,requests as rq,time, random,names
from discord.ext import commands
from discord.ext.commands import command
from ..Utils.util_func import random_color,edit_reason,list_breaker
import typing, names


class Channel(commands.Cog):
    """
    Channel related commands for managing your voice and text channels
    """
    def __init__(self,bot):
        self.bot=bot


    # delete by value, delete by filter and value
    @command()
    async def perms(self,msg,member:typing.Optional[discord.Member],chan:typing.Optional[discord.TextChannel]):
        """
        Check permissions of a user in a channel
        `Parameters`: perms(member:optional,channel:optional)
        `Ex`: s.perms @Cheng Yue #general-channel `or` s.perms
        `NOTE`: *If `member` or `chan` is not given, then it will use command user as target or command invoked channel as target*
        """

        if member is None:
            member = msg.author
        
        if chan is None:
            chan = msg.channel

        userPerms =  chan.permissions_for(member)

        emb = discord.Embed(color=await random_color(), description=f"{member.name}'s permissions in {chan.mention}")
        permList = {
            "Administrator" :userPerms.administrator,
            "Manage Channel": userPerms.manage_channels,
            "Add Reactions": userPerms.add_reactions,
            "Send Messages": userPerms.send_messages,
            "Manage Messages": userPerms.manage_messages,
            "Embed Links" :userPerms.embed_links,
            "Attach Files": userPerms.attach_files,
            "Read History": userPerms.read_message_history,
            "Create Invites": userPerms.create_instant_invite,
            "External Emojis": userPerms.external_emojis,
            "Mention Everyone": userPerms.mention_everyone
        }
        for key,value in permList.items():
            if value is True:
                emb.add_field(name=key,value='\✔')

        return await msg.send(embed=emb)

    @command(name='chan-members')
    async def chan_members(self,msg,chan:discord.TextChannel=None):
        """
        Check how many members can see a channel
        `CMD`: chan-members(channel:Optional)
        `Ex`: s.chan-members #cool-channel
        """
        if chan is None:
            chan = msg.channel

        return await msg.send(f"**{len(chan.members)}** Members can see the channel {chan.mention}")


    #NOTE: Channel Edit commands start----------
    @commands.has_permissions(manage_channels=True)
    @command(name='chan-name')
    async def chan_name(self,msg,chan:Optional[discord.TextChannel],*,newName = None):
        """
        Change the name of a channel
        `CMD`: chan-name(channel:Optional,new_name:Required)
        `Ex`: s.chan-name #old-channel cool-channel
        """
        if chan is None:
            chan = msg.channel

        if newName is None:
            return await msg.send(f"Please provide a new name for {chan.mention}.")

        oldName = chan.name
        await chan.edit(name=newName,reason=await edit_reason(msg.author,f"Channel name changed from {oldName} to {chan.name}"))
        return await msg.send(f"Channel **{oldName}** changed by {msg.author.name} to {chan.mention}")


    @commands.has_permissions(manage_channels=True)
    @command(name='chan-topic')
    async def chan_topic(self,msg,chan:typing.Optional[discord.TextChannel],*,newTopic = None):
        """
        Set or change the topic of a channel
        `CMD`: chan-topic(channel:Optional,newTopic:Required)
        `Ex`: s.chan-topic #bot-spam spam your bot commands in here
        """
        if chan is None:
            chan = msg.channel

        if newTopic is None:
            return await msg.send(f"Please enter topic details for {chan.mention}")

        await chan.edit(topic=newTopic,reason= await edit_reason(msg.author,f"Channel {chan.name} topic changed"))

        return await msg.send(f"{chan.mention}'s new topic set to **{newTopic}**")




    @commands.has_permissions(manage_channels=True)
    @command()
    async def nsfw(self,msg,chan:typing.Optional[discord.TextChannel],switch = None):
        """
        Turn on or off the NSFW mode for a text channel
        `CMD`: nsfw(chan:Optional,switch:Optional)
        `Ex`: s.nsfw #nsfw-chan on
        `NOTE`: *If no parameters are given, it will set it to the opposite of it's current value (NSFW will be false if initially on)*
        """
        if chan is None:
            chan = msg.channel

        isNSFW= chan.is_nsfw()
        if switch is None:
            await chan.edit(nsfw=not isNSFW,reason=await edit_reason(msg.author))
            return await msg.send(f"NSFW mode for {chan.mention} set to {not isNSFW}")

        if switch.lower() == 'on':
            switch = True

        if switch.lower() == 'off':
            switch = False

        if switch != 'on' and switch != 'off':
            return await msg.send(f"Unknown option {switch}.\nPlease enter `on` or `off` as the parameter")
    
        if isNSFW == switch and isNSFW is True:
            return await msg.send(f"NSFW mode for {chan.mention} is already on")

        if isNSFW == switch and isNSFW is False:
            return await msg.send(f"NSFW mode for {chan.mention} is already off")
        
        await chan.edit(nsfw = switch,reason=await edit_reason(msg.author))
        return await msg.send(f"NSFW mode for {chan.name} set to {switch}")


    @commands.has_permissions(manage_channels=True)
    @command(name='slow-mode')
    async def slow_mode(self,msg,chan:typing.Optional[discord.TextChannel],seconds:int = 60):
        """
        Enable slow mode for a channel
        `CMD`: slow-mode(channel:Optional,seconds:Optional)
        `Ex`: s.slow-mode #general 60
        `NOTE`: *the seconds can't be in decimal value. Putting 0 Seconds will disable it*
        """
        if chan is None:
            chan = msg.channel
        
        await chan.edit(slowmode_delay=seconds,reason= await edit_reason(msg.author))
        return await msg.send(f"Slowmode enabled for {chan.mention} for {seconds} seconds")


    @commands.has_permissions(manage_channels=True)
    @command(name='sync-perms')
    async def sync_perms(self,msg,chan:typing.Optional[discord.TextChannel],switch:str = None):
        """
        Sync channel's permission with its category
        `CMD` sync-perms(channel:Optional,switch:Optional)
        `Ex`: sync-perms #league-of-legends on
        `NOTE`: *If switch is not provided, it will default to True*
        """
        if chan is None:
            chan = msg.channel

        if switch is None:
            await chan.edit(sync_permissions=True)
            return await msg.send(f"Sync Permissions set to True for {chan.mention}")
        if switch.lower() == 'on':
            switch = True

        if switch.lower() == 'on':
            switch = False

        await chan.edit(sync_permissions=switch,reason=await edit_reason(msg.author))
        return await msg.send(f"Sync Permissions set to {switch} for {chan.mention}")



    @commands.has_permissions(manage_channels=True)
    @command(name='clone-chan')
    async def clone_chan(self,msg,chan:typing.Optional[typing.Union[discord.TextChannel,discord.VoiceChannel]],*,newName = None):
        """
        Clone a discord channel
        `CMD`: clone-chan(channel:Optional,new_name:Optional)
        `Ex`: s.clone-chan #general new-general `or` s.clone MusicVoice DJ Room🎵 *(Changes MusicVoice to DJ Room🎵)*
        `NOTE`: *You can clone both voice and text channels. If `new_name` is not provided, it will add `-clone` at the end of name*
        """

        if chan is None:
            chan = msg.channel

        if newName is None:
            newName = f"{chan.name}-clone"

        await chan.clone(name=newName,reason=await edit_reason(msg.author))
        return await msg.send(f"New clone channel {chan.name} created")





    async def large_delete(self,msg_list):
        for msg in msg_list:
            await msg.delete()



    @commands.cooldown(rate=1,per=300,type=commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True,read_message_history=True)
    @command(name='clear-msgs')
    async def purge_msg(self,msg,chan:typing.Optional[discord.TextChannel],amt:int = None):
        """
        Delete messages of a channel in bulk
        `CMD`: clear-msgs(channel:Optional,amount:Required)
        `Ex`: s.clear-msgs #bot-commands 2000
        `Cooldown`: 5 minutes cooldown `per use` ` server`
        `NOTE`: *Use this to delete large amounts of messages > 1000*
        """
        await msg.message.delete() #NOTE delete command message

        if chan is None:
            chan = msg.channel

        messages = await chan.history(limit=amt).flatten()
        new_list = await list_breaker(messages,4)
        func =asyncio.wait([self.large_delete(new_list[0]),self.large_delete(new_list[1]),self.large_delete(new_list[2]),self.large_delete(new_list[3])])
        await func
        return await msg.send(f"Messages cleared {msg.author.mention} ✅\nThis message will auto delete in 30 seconds",delete_after=30)


    @commands.cooldown(rate=1,per=120,type=commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True,read_message_history=True)
    @command(name='purge-msgs')
    async def purge_msg(self,msg,chan:typing.Optional[discord.TextChannel],amt = 100):
        """
        Purge messages of a channel
        `CMD`: purge-msgs(channel:Optional,amount:Optional)
        `Ex`: s.purge-msgs #bot-spam 230
        `Cooldown`: 2 minutes cooldown `per use` `per server`
        `NOTE`: *If `amount` max is 1000
        """
        if chan is None:
            chan = msg.channel

        
        if amt > 1000:
            amt = 1000

        await chan.purge(limit=amt)
        return await msg.send(f"Message purge complete ✅ {msg.author.mention}.\nThis message will auto delete after 30 seconds",delete_after=30)




    @commands.has_permissions(manage_webhooks=True)
    @command(name='check-hook')
    async def check_hook(self,msg,chan:typing.Optional[discord.TextChannel]):
        """
        Check if a webhook exist for a channel
        `CMD`: check-hook(channel:Optional)
        `Ex`: s.check-hook #announcements
        """
        if chan is None:
            chan = msg.channel

        web = await chan.webhooks()
        if not web:
            return await msg.send(f"No webhook found for {chan.mention}")
        
        if len(web) > 1:
            web = [hook.name for hook in web]
            return await msg.send(f"There are {len(web)} webhooks for {chan.mention}.\n{', '.join(web)}")
        
        return await msg.send(f"Found webhook {web.name} for {chan.name}")



    @commands.has_permissions(manage_webhooks=True)
    @command(name='create-webhook',aliases=['create-hook'])
    async def create_webhook(self,msg,chan:typing.Optional[discord.TextChannel],*,hookName= None,avatar = None):
        """
        Create a webhook for a channel
        `CMD`: create-webhook(channel:Optional,hook_name:Optional,avatar:Optional)
        `Ex`: s.create-webhook #commands captin-sender https://cdn.discordapp.com/attachments/671263788862930964/781360444194684958/21194257756_0791cfe2b1_o.jpg
        `NOTE`: *You can either upload the URL or upload the image along with command*
        """
        if chan is None:
            chan = msg.channel
        
        if hookName is None:
            name = names.get_full_name()

        if not avatar:
            hook = chan.create_webhook(name=hookName,avatar=avatar,reason=await edit_reason(msg.author))
            return await msg.send(f"Created new webhook named {hook.name}")
        


        hook = chan.create_webhook(name=hookName,reason=await edit_reason(msg.author))
        return await msg.send(f"A new webhook created with name {hook.name}")
        
        

    @commands.has_permissions(manage_channels=True)
    @command(name='del-chan')
    async def del_chan(self,msg,chan:typing.Optional[discord.TextChannel]):
        """
        Delete a chosen channel
        `CMD`: del-chan(channel:Optional)
        `Ex`: s.del-chan #bot-spam
        """
        if chan is None:
            chan = msg.channel

        await msg.send(f"The channel {chan.mention} will be deleted in 5 seconds")
        await asyncio.sleep(5)
        return await chan.delete()

    
    @commands.has_permissions(create_instant_invite=True)
    @command(name='create-invite',aliases=['invite'])
    async def create_invite(self,msg,use=0):
        #TODO: incomplete command
        """
        Create an invite for the server
        `CMD`: create-invite(uses:Optional)
        `Ex`: s.create-invite 4
        """
        invite = await msg.channel.create_invite(max_uses=use)
        return await msg.send(invite)


    #IMPORTANT: VOICE COMMAND START FROM HERE -----------------------------------------------------------------------
    @commands.has_permissions(manage_channels=True)
    @command(name='clone-voice')
    async def clone_voice(self,msg,*,chan:discord.VoiceChannel):
        """
        Clone a voice channel 
        `CMD`: clone-voice(chan:Required)
        `Ex:` s.clone-voice Music Party
        """
        clone=await chan.clone(name=f"{chan.name} Clone")
        return await msg.send(f"Cloned channel {clone.name}")

    @commands.has_permissions(manage_channels=True)
    @command(name="del-voice")
    async def delete_voice(self,msg,*,chan:discord.VoiceChannel):
        """
        Delete a voice channel
        `CMD`: del-voice(channel:Required)
        `Ex`: s.del-voice Music Party
        """
        await chan.delete()
        return await msg.send(f"Delete voice channel {chan.name}")


    @commands.has_permissions(manage_channels=True)
    @command(name="disconnect",aliases=['kick-voice','kickVoice'])
    async def kick_voice(self,msg,users:commands.Greedy[discord.Member]):
        """
        Kick/disconnect mentioned member(s) from a voice channel
        `CMD`: disconnect(users:Required)
        `Ex`: s.disconnect @Spam @Eggs, @Ham
        `Permissions`: Manage Channels
        """
        failed=[]
        for user in users:
            try:
                await user.move_to(channel=None)
            except Exception as Error:
                failed.append(user.name)
                print(Error, "disconnect CMD")

        if failed:
            await msg.send(f"Cold not disconnect user(s) {' '.join(failed)}")
        
        if failed > len(users):
            await msg.send(f"Cold not disconnect user(s) {' '.join(failed)}")

        return await msg.send("Disconnected users")




def setup(bot):
    bot.add_cog(Channel(bot))