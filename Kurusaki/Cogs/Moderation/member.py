import discord,asyncio,time,datetime,pymongo,names,typing,os
from discord.ext import commands
from discord.ext.commands import command



class Member(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.has_permissions(manage_roles=True)
    @command(aliases=['ar'])
    async def addrole(self,msg,opts:commands.Greedy[typing.Union[discord.Role,discord.Member]]):
        """
        Add mentioned role(s) to the mentioned user(s)
        `Ex:` .addrole @User1 @User2 @Role1 @Role2
        `Ex:` .addrole @Role1 @Role2 @User1 @User2
        `Ex:` .addrole @Role1 @Role2 @User1
        `Note:` Order doesn't matter as long as user and role is mentioned
        If no member mentioned then adds it to command user
        """
        roles=[role for role in opts if isinstance(role,discord.Role)]
        if not roles:
            return await msg.send(f"The mentioned role(s) or member(s) were not found\n{opts}")
        found_member=False
        for member in opts:
            if isinstance(member,discord.Member):
                found_member=True
                await member.edit(roles=member.roles+roles)

        if found_member == False:
            #No members mentioned
            await msg.author.edit(roles=msg.author.roles+roles)
        return await msg.message.add_reaction(emoji='✅')


    @commands.has_permissions(manage_roles=True)
    @command(aliases=['remove-role'])
    async def removeRole(self,msg,opts:commands.Greedy[typing.Union[discord.Role,discord.Member]]):
        """
        Remove mentioned role(s) to the mentioned user(s)
        `Ex:` .removerole @User1 @User2 @Role1 @Role2
        `Ex:` .removerole @Role1 @Role2 @User1 @User2
        `Note:` Order doesn't matter as long as user and role is mentioned
        """
        remove_roles=[role.id for role in opts if isinstance(role,discord.Role)]
        found_member=False
        new_roles=[]
        if not remove_roles:
            return await msg.send(f"The mentioned role(s) or member(s) were not found\n{opts}")
        for member in opts:
            if isinstance(member,discord.Member):
                found_member=True
                for role in member.roles:
                    if role.id not in remove_roles:
                        new_roles.append(role)
                await member.edit(roles=new_roles)

        if found_member == False:
            for role in msg.author.roles:
                if role.id not in remove_roles:
                    new_roles.append(role)
            await msg.author.edit(roles=new_roles)

        return await msg.message.add_reaction(emoji="✅")


    @commands.has_permissions(ban_members=True)
    @command()
    async def ban(self,msg,users:commands.Greedy[discord.Member],*,reason=None):
        """
        Ban member(s) who are mentioned and give an optional reason at the end of the mentions.
        `Ex:` .ban @Member1 @Member2 For breaking the rules
        `Ex:` .ban @Member1
        `Permissions:` Administrator or Ban Members
        If mentioned member is not found, it'll skip it
        """
        for user in users:
            await user.ban(reason=reason)
        return await msg.send(f"Banned user(s) {' '.join([user.name for user in users])}")
                              
    @commands.has_permissions(ban_members=True)
    @command()
    async def unban(self, ctx, _id: int):
        """
        Unbans a member with a given ID
        `Ex:` .unban 392839428348
        `Permission:` Ban Members
        """
        user = self.bot.get_user(_id)
        try:
            await ctx.guild.unban(user)
        except:
            if user is None:
                return await ctx.send(f"The user with the ID: {_id} does not exist")
            return await ctx.send("Something went wrong ")
        
        emb = discord.Embed(colour=0x419400, description=f"<:yees:695487080750383115> {user.name} has been unbanned")
        await ctx.send(embed=emb)


    @commands.has_permissions(kick_members=True)
    @command()
    async def kick(self,msg,users:commands.Greedy[discord.Member],reason=None):
        """
        Kick members that are mentioned and give an optional reason at the end.
        `Ex:` .kick @Member1 @Member2
        `Ex:` .kick @Member1 @Member2 Broke server roles
        `Permissions:` Kick Members
        """
        for user in users:
            await user.kick(reason=reason)

        await msg.send(f"Kicked user(s) {' '.join([user.name for user in users])}")


    @commands.has_permissions(mute_members=True)
    @command(aliases=['m'])
    async def mute(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server mute the mentioned member(s) in voice channels
        `Ex:` .mute @Member1 @Member2
        `Permissions:` Mute Members
        """
        for user in users:
            await user.edit(mute=True)
        return await msg.send(f"Server muted user(s) `{' '.join([user.name for user in users])}`")


    @commands.has_permissions(mute_members=True,administrator=True)
    @command(aliases=['unMute'])
    async def un_mute(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server un-mute mentioned member(s) in voice channels
        `Ex:` .unMute @Member1 @Member2
        `Permissions:` Mute Members
        """
        for user in users:
            await user.edit(mute=False)
        return await msg.send(f"Server un-muted user(s) `{' '.join([user.name for user in users])}`")


    @commands.has_permissions(deafen_members=True,administrator=True)
    @command(aliases=['deaf'])
    async def deafen(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server deafen mentioned member(s) in voice channels
        `Ex:` .deafen @Member1 @Member2
        `Permissions:` Deafen Members
        """
        for user in users:
            await user.edit(deafen=True)
        return await msg.send(f"Server deafened user(s) `{' '.join([user.name for user in users])}`")


    @commands.has_permissions(deafen_members=True,administrator=True)
    @command(aliases=['und','un-deafen'])
    async def unDeafen(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server deafen mentioned member(s) in voice channels
        `Ex:` .unDeafen @Member1 @Member2
        `Permissions:` Deafen Members
        """
        for user in users:
            await user.edit(deafen=False)

        return await msg.message.add_reaction(emoji='✅')



    @commands.has_permissions(move_members=True)
    @command(aliases=['move-to'],enabled=False,hidden=True)
    async def moveTo(self,msg,users:commands.Greedy[discord.Member],chan:discord.VoiceChannel):
        #TODO: Check if mentioned members are in voice channel first
        """
        Move member(s) to a different voice channel
        `Ex:` .moveto @Member1 @Member2 Voice Channel Name
        `Permissions:` Move Members
        """
        no_voice=[]
        for user in users:
            if user.voice:
                #User in voice channel?
                pass
            await user.move_to(chan,reason=f'Command used by {msg.author.name}({msg.author.id})')

        return await msg.message.add_reaction(emoji='✅')




    @commands.has_permissions(manage_nicknames=True)
    @command(aliases=['changenick','change-nick'])
    async def changenickname(self,msg,users:commands.Greedy[discord.Member],*,name=None):
        """
        Change the server name of mentioned member(s
        `Ex:` .changenickname @Member1 @Member2 Hunters
            `Note:` All mentioned members' name will now be Hunters
        `Permissions:` Manage Nicknames
        """
        before=users
        if name is not None:
            for user in users:
                await user.edit(nick=name)

            return await msg.message.add_reaction(emoji='✅')
        
        for user in users:
            await user.edit(nick=None)
        
        return await msg.message.add_reaction(emoji='✅')


    @commands.has_permissions(manage_channels=True)
    @command(aliases=['kick-voice','kickVoice'])
    async def kick_voice(self,msg,users:commands.Greedy[discord.Member]):
        """
        Kick mentioned member(s) from a voice channel
        `Ex:` .kick-voice @Member1 @Member2
        `Permissions:` Manage Channels
        """
        for user in users:
            await user.edit(voice_channel=None)
        return await msg.message.add_reaction(emoji='✅')




def setup(bot):
    bot.add_cog(Member(bot))
