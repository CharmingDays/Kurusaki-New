import discord,asyncio,requests as rq,time, random,names
from discord.ext import commands
from discord.ext.commands import command,Cog


class TextChannel(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    @commands.cooldown(per=20,rate=2,type=commands.BucketType.guild)
    @command(name='chan-msgs')
    async def channelMessages(self,msg,user:discord.Member=None):
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
    async def servermessages(self,msg,user:discord.Member=None):
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



    @commands.group(name='msg')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def msg_manage(self,msg):
        if msg.invoked_subcommand is None:
            return msg.send(msg.command.help)
            


    @commands.is_owner()
    @msg_manage.command(hidden=True)
    async def clear(self,msg,_limit=100):
        """
        Clears 100 messages inside the text channel
        `Ex:` .clear
        
        """
        if _limit >= 2000:
            _limit=2000
            await msg.send("Purge limit has exceeded 2000")
        await msg.channel.purge(limit=_limit)
        return await msg.message.add_reaction(emoji='✅')

    @commands.has_permissions(manage_channels=True)
    @command(name='tname',aliases=['channel-name','chan-name'])
    async def channel_name(self,msg,*,newName=None):
        if newName is None:
            newName=f'new-channel-name{random.randint(2,55)}'
        await msg.channel.edit(name=newName,reason=f"Command used by {msg.author.name}({msg.author.id})")
        await msg.send(f"Channel {msg.channel.name} is now called **{newName}**",delete_after=230)

    @commands.has_permissions(manage_channels=True)
    @command(name='set-topic',aliases=['s-topic'])
    async def set_topic(self,msg,*,new_topic):
        await msg.channel.edit(topic=new_topic,reason=f'Command used by {msg.author.name}({msg.author.id})')
        await msg.send(f"Topic channel changed to {new_topic}",delete_after=230)



    
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def nsfw(self,msg,mode:str=None):
        if mode is None:
            if msg.channel.is_nsfw() is True:
                return await msg.send(f"NSFW is already enabled for {msg.channel.name}",delete_after=120)
            
            if msg.channel.is_nsfw() is False:
                await msg.edit(nsfw=True)
                return await msg.message.add_reaction(emoji='✅')

        if mode.lower() == 'off':
            await msg.channel.edit(nsfw=False,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Channel NSFW {mode}",delete_after=230)

        if mode.lower() == 'on':
            await msg.channel.edit(nsfw=True,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send("**NSFW mode on**",delete_after=230)



    @commands.has_permissions(manage_channels=True)
    @command(name='syncperms')
    async def sync_perms(self,msg,switch:str):
        if switch.lower() =='on':
            await msg.channel.edit(sync_permissions=False,reason=f'Command used by {msg.author.name}({msg.author.id})')
            return await msg.send(f"`{msg.channel.name}` permissions synced to **{msg.channel.category.name}**",delete_after=230)

        if switch.lower() =='off':
            await msg.channel.edit(sync_permissions=False,reason=f'Command used by {msg.author.name}({msg.author.id})')
            return await msg.send(f"`{msg.channel.name}` permissions sync turned off for **{msg.channel.category.name}**",delete_after=230)





    @commands.has_permissions(manage_channels=True)
    @command(aliases=['smode'])
    async def slowmode(self,msg,switch:str=None,amt:int=10):
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
                await msg.send("Amount exceeds limit, delay set to max value 21600 seconds (6 hours)",delete_after=230)
            
            else:
                await msg.channel.edit(slowmode_delay=amt)

                return await msg.send(f"Slowmode set to {amt} seconds)",delete_after=230)

        if switch.lower() == 'off':
            await msg.channel.edit(slowmode_delay=0)
            await msg.send(f"Slowmode turned off for `{msg.channel.name}`",delete_after=230)


    @msg_manage.command()
    async def clone(self,msg,newName=None,chan:discord.TextChannel=None):
        if newName is None:
            newName=msg.channel.name
    
        if chan is None:
            await msg.channel.clone(name=newName,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Channel `{msg.channel.name}` cloned and named **{newName}**",delete_after=230)


        if chan is not None:
            await chan.clone(name=newName,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Channel `{chan.name}` cloned and named **{newName}**",delete_after=230)



    @msg_manage.command(name='clear-chan',aliases=['clear-channel'])
    async def clear_channel(self,msg,*channels:discord.TextChannel):
        if channels:
            for chan in channels:
                await chan.clone(name=chan.name)
                await chan.delete(reason=f'Command used by {msg.author.name}({msg.author.id})')
                await msg.send(f"Channel {chan.name} cleared")


        else:
            await msg.channel.clone(name=msg.channel.name)
            await msg.channel.delete(reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Channel **{msg.channel.name}** cleared",delete_after=230)



    @commands.has_permissions(manage_webhooks=True)
    @command(name='create-webhook',aliases=['make-webhook','create-hook','make-hook'])
    async def create_webhook(self,msg,name=None):
        if name is None:
            web=await msg.channel.create_webhook(name=names.get_first_name(),reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Webhook {web.name} created for {web.channel.name}",delete_after=230)

        if name is not None:
            web=await msg.channel.create_webhook(name=name,reason=f'Command used by {msg.author.name}({msg.author.id})')
            await msg.send(f"Webhook {web.name} created for {web.channel.name}",delete_after=230)



    @commands.has_guild_permissions(create_instant_invite=True)
    @command(name='create-invite',aliases=['make-inv','create-inv','invite'])
    async def create_invite(self,msg,mode='temp'):
        if mode.lower() =='temp':
            link=await msg.channel.create_invite(temporary=True)
            await msg.send(link)
        if mode.lower() == 'perm':
            link=await msg.channel.create_invite(temporary=False)
            await msg.send(link)
    
    @commands.has_permissions(manage_channels=True)
    @command(name='delete-channel',aliases=['del-chan'])
    async def delete_channel(self,msg,chan:discord.TextChannel=None):
        if chan is not None:
            await msg.send(f"Deleting {chan.name}...",delete_after=5)
            await chan.delete()

        if chan is None:
            await msg.send(f"Deleting channel {msg.channel.name}...")
            await asyncio.sleep(1)
            await msg.channel.delete(reason=f'Command used by {msg.author.name}({msg.author.id})')


    @commands.has_permissions(manage_guild=True)
    @command(aliases=['view-invites','server-invites','guild-invites'])
    async def invites(self,msg):
        emb=discord.Embed(title='Invites')
        codes=await msg.send(msg.channel.invites())
        emb.set_footer(text=msg.guild.name,icon_url=msg.guild.icon_url) #TODO: Needs to include guild's url
        for i in codes:
            emb.add_field(name=i.inviter.name,value=i.id)

        await msg.send(embed=emb,delete_after=120)


    # #!-------PURGE COMMANDS START HERE-----------!
    # #!-------GROUP COMMANDS START HERE-----------!
    # #!-----THIS IS ALL BROKEN----------!
    # @commands.group(aliases=['purge'])
    # @commands.guild_only()
    # @commands.has_permissions(manage_messages=True)
    # async def clear(self, ctx):
    # #!---NOTE-----!: I HAVE NO CLUE WHAT THIS CODE OR COMMAND DOES
    # #!---NOTE-----!: PLEASE FIX IT OR GIVE A PROPER DOCUMENTATION ON IT VZY!
    #     """
    #     The group definition for the sub-commands below
    #     """

    #     if ctx.invoked_subcommand is None:
    #         await ctx.send_help(ctx.command)

    # async def remove_messages(self, ctx, limit, predicate, *, before=None, after=None):
    #     if limit > 2000:
    #         return await ctx.send(f'<:no:699364582766018670> Too many messages to search given ({limit}/2000)')

    #     if before is None:
    #         before = ctx.message
    #     else:
    #         before = discord.Object(id=before)

    #     if after is not None:
    #         after = discord.Object(id=after)

    #     try:
    #         deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
    #     except discord.Forbidden as e:
    #         return await ctx.send('<:no:699364582766018670> I do not have permissions to delete messages.')
    #     except discord.HTTPException as e:
    #         return await ctx.send(f'<:no:699364582766018670> Error: {e} (try a smaller search?)')

    #     spammers = Counter(m.author.display_name for m in deleted)
    #     deleted = len(deleted)
    #     messages = [f'{deleted} message{" was" if deleted == 1 else "s were"} removed.']
    #     if deleted:
    #         messages.append('')
    #         spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
    #         messages.extend(f'<:CheckMark:699364294160154624> **{name}**: {count}' for name, count in spammers)

    #     to_send = '\n'.join(messages)

    #     if len(to_send) > 2000:
    #         await ctx.send(f'<:CheckMark:699364294160154624> Successfully removed {deleted} messages.', delete_after=10)
    #     else:
    #         await ctx.send(to_send, delete_after=10)




    # @clear.command()
    # async def images(self, ctx, search=100):
    #     """
    #     Removes messages that have embeds or attachments.
    #     `Ex:` .clear images
    #     """
    #     await self.remove_messages(ctx, search, lambda e: len(e.embeds) or len(e.attachments))


    # @clear.command(name='remove-all')
    # async def _remove_all(self, ctx, search=100):
    #     """
    #     Removes all messages.
    #     Usage: .clear all
    #     """
    #     await self.remove_messages(ctx, search, lambda e: True)


    # @clear.command()
    # async def user(self, ctx, member: discord.Member, search=100):
    #     """Removes all messages by the member.
    #     `Ex`: .clear @mrbutter#7753
    #     """
    #     await self.remove_messages(ctx, search, lambda e: e.author == member)



    # @clear.command()
    # async def contains(self, ctx, *, substr: str):
    #     """
    #     Removes all messages containing a substring. The substring must be at least 3 characters long.
    #     `Ex:` .clear contains abc
    #     """
    #     if len(substr) < 3:
    #         await ctx.send('<:no:699364582766018670> The substring length must be at least 3 characters.')
    #     else:
    #         await self.remove_messages(ctx, 100, lambda e: substr in e.content)



def setup(bot):
    bot.add_cog(TextChannel(bot))

#TODO: All the functions need additional fix
