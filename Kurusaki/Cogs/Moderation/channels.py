import discord,asyncio,requests as rq,time, random,names
from discord.ext import commands
from discord.ext.commands import command,Cog


class Channel(commands.Cog):
    """
    Channel related commands for managing your voice and text channels
    """
    def __init__(self,bot):
        self.bot=bot


    @commands.cooldown(per=20,rate=2,type=commands.BucketType.guild)
    @command(name='chan-msgs')
    async def channelMessages(self,msg,user:discord.Member=None):
        """
        Check how many messages have been sent by mentioned user in the channel.
        `Ex:` s.chan-msgs @User
        `Note:` Has a cooldown of 20 seconds for entire server per use
        """
        amts=0
        await msg.send(f"Processing {msg.channel.mention}'s messages...")
        package=await msg.channel.history(limit=None).flatten()
        if user is None:
            await msg.send(f"Selecting {msg.author.name}'s messages in {msg.channel.mention}")
            for i in package:
                if i.author.id == msg.author.id:
                    amts+=1
            await msg.send(f"{amts}/{len(package)} messages sent by {msg.author.name} in {msg.channel.name}")
        if user is not None:
            await msg.send(f"Selecting {user.name}'s messages in {msg.channel.mention}")
            for i in package:
                if i.author.id == user.id:
                    amts+=1

            await msg.send(f"{amts}/{len(package)} messages sent by {user.name} in {msg.channel.name}")

        

    @commands.cooldown(per=60,rate=1,type=commands.BucketType.guild)
    @command(name='server-msgs')
    async def serverMessages(self,msg,user:discord.Member=None):
        """
        Check the amount oof messages sent in the server from the mentioned user.
        `Ex:` s.server-msgs @User
        `Note:` Has a cooldown of 60 seconds for entire server per use
        """
        amts=0
        await msg.send(f"Processing {msg.guild.name} messages...")
        channels=[await chan.history(limit=None).flatten() for chan in msg.guild.text_channels]
        total=0
        if user is None:
            await msg.send(f"Counting {msg.author.name}'s messages in {msg.guild.name}")
            for i in channels:
                for x in i:
                    total+=1
                    if x.author.id == msg.author.id:
                        amts+=1

            await msg.send(f"{amts}/{total} messages send by {msg.author.name} in {msg.guild.name}")

        if user is not None:
            await msg.send(f"Counting {user.name}'s messages in {msg.guild.name}")
            for i in channels:
                for x in i:
                    total+=1
                    if x.author.id == user.id:
                        amts+=1

            await msg.send(f"{amts}/{total} messages send by {user.name} in {msg.guild.name}")


    # @commands.group(name='msg')
    # @commands.guild_only()
    # @commands.has_permissions(manage_messages=True)
    # async def msg_manage(self,msg):
    #     if msg.invoked_subcommand is None:
    #         return msg.send(msg.command.help)
            


    @commands.has_permissions(manage_messages=True,read_message_history=True)
    @command(name='clear-msgs')
    async def clear_messages(self,msg,_limit=100):
        """
        Purges (deletes) the given amount of messages
        `Ex:` .clear-msgs
        `Note:` Has a limit of 2000 and messages must not be older than 14 days.
        `Permissions:` Manage Messages
        """
        await msg.send("Please wait while the bot tries to delete all possible messages")
        if _limit >= 2000:
            _limit=2000
            await msg.send("Purge limit has exceeded 2000, setting new limit to 2000")
        await asyncio.sleep(3)
        await msg.channel.purge(limit=_limit)
        return await msg.send(f'{msg.author.mention} ✅',delete_after=20) #NOTE: Can't use reaction as it deletes the messages



    @commands.has_permissions(manage_channels=True)
    @command(name='text-name',aliases=['channel-name','chan-name'])
    async def channel_name(self,msg,*,newName=None):
        """
        Change name of the text channel where command is used
        `Ex:` s.text-name New-General
        `Permissions:` Manage Channels
        """
        if newName is None:
            newName=f'new-channel-name{random.randint(2,55)}'
        await msg.channel.edit(name=newName,reason=f"Command used by {msg.author.name}({msg.author.id})")
        await msg.send(f"Channel {msg.channel.name} is now called **{newName}**")


    @commands.has_permissions(manage_channels=True)
    @command(name='set-topic',aliases=['s-topic'])
    async def set_topic(self,msg,*,new_topic):
        """
        Set a topic for the channel or change it
        `Ex:` s.set-topic A channel for sending memes or troll contents
        `Permissions:` Manage Channels
        """
        await msg.channel.edit(topic=new_topic,reason=f'Command used by {msg.author.name}({msg.author.id})')
        await msg.send(f"Topic channel changed to {new_topic}")




    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def nsfw(self,msg,mode:str=None):
        """
        Turn on or off Not Safe For Work (NSFW) for the channel
        `Ex:` s.nsfw off
        `Ex:` s.nsfw on
        `Permissions:` Manage Channels
        """
        if mode is None:
            if msg.channel.is_nsfw() is True:
                return await msg.send(f"NSFW is already enabled for {msg.channel.name}")
            
            if msg.channel.is_nsfw() is False:
                await msg.edit(nsfw=True)
                return await msg.message.add_reaction(emoji='✅')

        if mode.lower() == 'off':
            await msg.channel.edit(nsfw=False,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Channel NSFW {mode}")

        if mode.lower() == 'on':
            await msg.channel.edit(nsfw=True,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send("**NSFW mode on**")



    @commands.has_permissions(manage_channels=True)
    @command(name='sync-perms')
    async def sync_perms(self,msg,switch:str):
        """
        Sync the channel's permissions with the category it's in
        `Ex:` s.sync-perms
        `Permissions:` Manage Channels
        """
        if switch.lower() =='on':
            await msg.channel.edit(sync_permissions=False,reason=f'Command used by {msg.author.name}({msg.author.id})')
            return await msg.send(f"`{msg.channel.name}` permissions synced to **{msg.channel.category.name}**")

        if switch.lower() =='off':
            await msg.channel.edit(sync_permissions=False,reason=f'Command used by {msg.author.name}({msg.author.id})')
            return await msg.send(f"`{msg.channel.name}` permissions sync turned off for **{msg.channel.category.name}**")

        return await msg.send(f"Unknown keyword {switch}.**Please specify** `on` **or** `off`")



    @commands.has_permissions(manage_channels=True)
    @command(aliases=['smode'])
    async def slowmode(self,msg,switch:str=None,amt:int=10):
        """
        Enable slowmode for the text channel
        `Ex:` s.smode on/off 434
        `Permissions:` Manage Channels
        """
        if switch is None:
            if msg.channel.slowmode_delay == 0:
                await msg.channel.edit(slowmode_delay=amt)
                return await msg.send(f"Enabled slowmode_delay to {amt} seconds as default for {msg.channel.name}")
            if msg.channel.slowmode_delay != 0 and amt != 10:
                await msg.channel.edit(slowmode_delay=amt)
                return await msg.send(f"Enabled slowmode_delay to {amt} seconds for {msg.channel.name}")

            if msg.channel.slowmode_delay != 0 and amt == 10:
                await msg.edit(slowmode_delay=0)
                return await msg.send(f"Slow mode disabled for {msg.channel.name}")

        if switch.lower() == 'on':
            if amt > 21600:
                amt = 21600
                await msg.channel.edit(slowmode_delay=amt)
                await msg.send("Amount exceeds limit, delay set to max value 21600 seconds (6 hours)")
            
            else:
                await msg.channel.edit(slowmode_delay=amt)

                return await msg.send(f"Slowmode set to {amt} seconds)")

        if switch.lower() == 'off':
            await msg.channel.edit(slowmode_delay=0)
            await msg.send(f"Slowmode turned off for `{msg.channel.name}`")

    @commands.has_permissions(manage_channels=True)
    @command()
    async def clone(self,msg,new_name=None,chan:discord.TextChannel=None):
        """
        Clone a specific channel or the current one with specific name or same name
        `Ex:` s.clone general-chat-clone #general
        `Note:` values must be in order of (name,channel to clone)
        `Note:` If no new name is provided default name is used, without channel to clone mentioned it'll clone current one
        `Command:` clone(new-Name,channel-To-Clone)
        """
        if new_name is None:
            new_name=f"clone-{msg.channel.name}"
    
        if chan is None:
            await msg.channel.clone(name=new_name,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Channel `{msg.channel.name}` cloned and named **{new_name}**",)


        if chan is not None:
            await chan.clone(name=new_name,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Channel `{chan.name}` cloned and named **{new_name}**")


    @commands.has_permissions(manage_messages=True)
    @command(name='clear-chan',aliases=['clear-channel'])
    async def clear_channel(self,msg,*channels:discord.TextChannel):
        """
        Clear all the messages in a channel or a specific one
        `Ex:` s.clear-chan #bot-spam #meme-spam (To clear both #bot-spam and #meme-spam)
        `Ex:` s.clear-chan (To clear the current channel where command is used)
        `Permissions:` Manage Messages
        `Command:` clear-chan(channel-names-mentioned:list)
        """
        if channels:
            for chan in channels:
                new_chan=await chan.clone(name=chan.name)
                await chan.delete(reason=f'Command used by {msg.author.name}({msg.author.id})')
                await new_chan.send(f"Channel {chan.name} cleared")


        else:
            new_chan=await msg.channel.clone(name=msg.channel.name)
            await msg.channel.delete(reason=f'Command used by {msg.author.name}({msg.author.id})')
            await new_chan.send(f"Channel **{msg.channel.name}** cleared")



    @commands.has_permissions(manage_webhooks=True)
    @command(name='create-webhook',aliases=['make-webhook','create-hook','make-hook'])
    async def create_webhook(self,msg,name=None):
        """
        Create a webhook for the current channel
        `Ex:` s.create-webhook CaptainWebhook
        `Permissions:` Manage Webhooks
        `Command:` create-webhook(webhook-Name)
        """
        if name is None:
            web=await msg.channel.create_webhook(name=names.get_first_name(),reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Webhook {web.name} created for {web.channel.name}")

        if name is not None:
            web=await msg.channel.create_webhook(name=name,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Webhook {web.name} created for {web.channel.name}")



    @commands.has_guild_permissions(create_instant_invite=True)
    @command(name='create-invite',aliases=['make-inv','create-inv'])
    async def create_invite(self,msg,mode='temp'):
        """
        Create an invite link for the current channel
        `Ex:` s.create-invite temp/perm (If not specifyied, it'll be temp)
        `Permissions:` Create Instant Invites
        `Command:` create-invite(mode:temp/perm:optional)
        """
        if mode.lower() =='temp':
            link=await msg.channel.create_invite(temporary=True)
            await msg.send(link)
        if mode.lower() == 'perm':
            link=await msg.channel.create_invite(temporary=False)
            await msg.send(link)
    


    @commands.has_permissions(manage_channels=True)
    @command(name='delete-channel',aliases=['del-chan'])
    async def delete_channel(self,msg,chan:discord.TextChannel=None):
        """
        Delete the current channel or a specific channel
        `Ex:` s.delete-channel #memes-troll (If no channel is mentioned, it'll delete the channel of command being used at)
        `Permissions:` Manage Channels
        `Command:` delete-channel(channel-mentioned:TextChannel|optional)
        """
        if chan is not None:
            await msg.send(f"Deleting {chan.name}...")
            await chan.delete()

        if chan is None:
            await msg.send(f"Deleting channel {msg.channel.name}...")
            await asyncio.sleep(1)
            await msg.channel.delete(reason=f'Command used by {msg.author.name}({msg.author.id})')



    #!-----------VOICE CHANNEL COMMADDS START HERE --------------!
    def cancel_voice():
    #pylint: disable=no-method-argument
    #Python: disable=no-method-argument
        def predicate(msg):
            if msg.author.voice:
                return 'sleep' in msg.author.voice.channel.name.lower()

        return commands.check(predicate)



def setup(bot):
    bot.add_cog(Channel(bot))

#TODO: All the functions need additional fix
