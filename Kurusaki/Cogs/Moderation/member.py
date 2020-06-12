import discord,asyncio,time,datetime,pymongo,names,typing,os
from discord.ext import commands
from discord.ext.commands import command



class Member(commands.Cog):
    """
    Member related commands to mange them
    """
    def __init__(self,bot):
        self.bot=bot


    @commands.has_permissions(manage_roles=True)
    @command(aliases=['add-role'])
    async def addrole(self,msg,opts:commands.Greedy[typing.Union[discord.Role,discord.Member]]):
        """
        Add mentioned role(s) to the mentioned user(s)
        `Ex:` .addrole @User1 @User2 @Role1 @Role2
        `Ex:` .addrole @Role1 @Role2 @User1 @User2
        `Note:` Order must be roles --> users or users---> roles
        If no member mentioned then adds it to command user
        """
        roles=[role for role in opts if isinstance(role,discord.Role)]
        if not roles:
            return await msg.send(f"The mentioned role(s) or member(s) were not found\n{opts}")
        found_member=False
        for member in opts:
            if isinstance(member,discord.Member):
                #NOTE: member mentioned
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
    @command(aliases=['banish'])
    async def ban(self,msg,*users:discord.Member):
        """
        Ban out the mentioned users
        `Ex:` s.ban @User1 @User2 @User3
        `Permissions:` Ban Members
        `Command:` ban(users:list)
        """
        if not users:
            return await msg.send("Please mention the user(s) to ban from the server")
        
        if users:
            banned=[]
            failed=[]
            for user in users:
                try:
                    await msg.guild.ban(user=user)
                    banned.append(user.name)
                except:
                    failed.append(user.name)

            if banned:
                await msg.send(f"Banned the following members from the server {', '.join(banned)}")

            if failed:
                await msg.send(f"Failed to ban the following members {', '.join(failed)}")



    @commands.has_permissions(kick_members=True)
    @command(aliases=['boot'])
    async def kick(self,msg,*users:discord.Member):
        """
        Kick out the mentioned users
        `Ex:` s.kick @User1 @User2 @User3
        `Permissions:` Kick Members
        `Command:` kick(users:list)
        """

        if not users:
            return await msg.send("Please enter the name of the user(s) to kick from the server or mention them.")

        if users:
            booted=[]
            failed=[]
            for user in users:
                try:
                    await msg.guild.kick(user=user)
                    booted.append(user.name)
                except:
                    failed.append(user.name)

            if booted:
                await msg.send(f"Booted {', '.join(booted)}")

            if failed:
                await msg.send(f"Failed to kick the members {', '.join(failed)}")



    @commands.has_permissions(mute_members=True)
    @command(aliases=['silence'])
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
    @command(name='un-mute',aliases=['unmute'])
    async def un_mute(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server un-mute mentioned member(s) in voice channels
        `Ex:` .un-mute @Member1 @Member2 (Can mention more than 1 user)
        `Permissions:` Mute Members
        `Command:` un-mute(users:list)
        """
        for user in users:
            await user.edit(mute=False)
        return await msg.send(f"Server un-muted user(s) `{' '.join([user.name for user in users])}`")


    @commands.has_permissions(deafen_members=True,administrator=True)
    @command(aliases=['deaf'])
    async def deafen(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server deafen mentioned member(s) in voice channels
        `Ex:` .deafen @Member1 @Member2 (Can mention more than 1 user)
        `Permissions:` Deafen Members
        `Command:` deafen(users:list)
        """
        for user in users:
            await user.edit(deafen=True)
        return await msg.send(f"Server deafened user(s) `{' '.join([user.name for user in users])}`")


    @commands.has_permissions(deafen_members=True,administrator=True)
    @command(name='un-deafen')
    async def unDeafen(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server deafen mentioned member(s) in voice channels
        `Ex:` .un-deafen @Member1 @Member2
        `Permissions:` Deafen Members
        `Command:` un-deafen(users:list)
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
        `Ex:` .moveto @Member1 @Member2 League of Legends
        `Permissions:` Move Members
        `Command:` move-to(users:list,chan:required)
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
        Change the server name of mentioned member(s)
        `Ex:` .changenickname @Member1 @Member2 Hunters (All mentioned members' name will now be Hunters)
        `Permissions:` Manage Nicknames
        `Command:` changenick(users:list, new-name)
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
        `Command:` kick-voice(users:list)
        """
        for user in users:
            await user.edit(voice_channel=None)
        return await msg.message.add_reaction(emoji='✅')




def setup(bot):
    bot.add_cog(Member(bot))
