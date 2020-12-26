from discord.ext import commands
from discord.ext.commands import command
from ..Utils.util_func import random_color
import discord, asyncio
import time, datetime
import pymongo, names, string
import typing, os ,random



class Member(commands.Cog):
    """
    Member related commands to mange them
    """
    def __init__(self,bot):
        self.bot=bot


    @command(name='user-info')
    async def user_info(self,msg,user:discord.Member=None):
        """
        Retrive a user's info
        `CMD`: user-info(user:Optional)
        `Ex:` s.user-info @Cheng Yue
        `NOTE`: If user is provided, command user will be user
        """
        if user is None:
            user = msg.author

        emb=discord.Embed(title=f"{user} - {user.id}",color=self.random_color)
        date=user.joined_at
        ac_date=user.created_at
        emb.set_thumbnail(url=user.avatar_url)
        emb.add_field(name='Created At',value=f"{ac_date.month}/{ac_date.day}/{ac_date.year} - {ac_date.hour}:{ac_date.minute}")
        emb.add_field(name='Joined Date',value=f"{date.month}/{date.day}/{date.year} - {date.hour}:{date.minute} UTC")
        emb.add_field(name="Rop Role",value=user.top_role)
        emb.add_field(name='Roles',value=", ".join([role.name for role in user.roles]))
        emb.add_field(name="Status",value=user.status,inline=False)
        return await msg.send(embed=emb)



    @commands.has_permissions(manage_roles=True)
    @command(aliases=['add-role'])
    async def addrole(self,msg,opts:commands.Greedy[typing.Union[discord.Role,discord.Member]]):
        """
        Add role(s) to a given member
        `CMD`: addRole(user:Required,role:Required)
        `Ex:` s.addrole @Cheng Yue @Member
        `Permission`: Manage Roles
        `NOTE`: You can mention user first or role first, order doesn't matter.
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
        Remove role(s) from a user(s)
        `CMD`: removeRole(user:Required,role:Required)
        `Ex:` s.removeRole
        `Permission`: Manage Roles
        `NOTE`: You can mention role or user first, order doesn't matter.
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
        Ban user(s) mentioned
        `CMD`: ban(user:Required)
        `Ex:` s.ban @Spam @Egg
        `Permission`: Ban Members
        """


    @commands.has_permissions(kick_members=True)
    @command(aliases=['boot'])
    async def kick(self,msg,*users:discord.Member):
        """
        Kick user(s) mentioned
        `CMD`: kick(user:Required)
        `Ex:` s.kick @Ham, @Spam
        `Permission`: Kick Members
        """


    @commands.has_permissions(mute_members=True)
    @command(aliases=['silence'])
    async def mute(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server mute the mentioned member(s) in voice channels
        `CMD`: mute(user:Required)
        `Ex`: s.mute @Spam @Eggs
        `Permissions`: Mute Members
        """
 

    @commands.has_permissions(mute_members=True,administrator=True)
    @command(name='un-mute',aliases=['unmute'])
    async def un_mute(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server un-mute mentioned member(s) in voice channels
        `CMD`: s.un-mute(user:Required)
        `Ex`: s.un-mute @Spam @Ham 
        `Permissions`: Mute Members
        """


    @commands.has_permissions(deafen_members=True,administrator=True)
    @command(aliases=['deaf'])
    async def deafen(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server deafen mentioned member(s) in voice channels
        `CMD`: deafen(users:Required)
        `Ex`: s.deafen @Eggs @Spam
        `Permissions`: Deafen Members
        """


    @commands.has_permissions(deafen_members=True,administrator=True)
    @command(name='un-deafen')
    async def unDeafen(self,msg,users:commands.Greedy[discord.Member]):
        """
        Server deafen mentioned member(s) in voice channels
        `CMD`: un-deafen(users:Required)
        `Ex:` .un-deafen @Eggs @Spam
        `Permissions`: Deafen Members
        """


    @commands.has_permissions(move_members=True)
    @command(aliases=['move-to'],enabled=True,hidden=True)
    async def moveTo(self,msg,users:commands.Greedy[discord.Member],chan:discord.VoiceChannel):
        #TODO: Check if mentioned members are in voice channel first
        """
        Move member(s) to a different voice channel
        `CMD`: move-to(users:Required,Voice channel:Required)
        `Ex`: .moveto @Spam @Eggs League of Legends VC
        `Permissions`: Move Members
        """



    @commands.has_permissions(manage_nicknames=True)
    @command(aliases=['changename','change-nick'])
    async def changeNick(self,msg,users:commands.Greedy[discord.Member],*,name=None,nameType:str=None):
        """
        Give the selected member(s) a new sever nickname
        `CMD`: changeNick(users:list, new-name)
        `Ex`: s.changenickname @Spam @Eggs Hunters number ("Spam,Eggs" --> "Hunter1, Hunger2")
        `Permissions`: Manage Nicknames
        `NOTE`: If new name is not given, random name will be selected
        If nameType is not selected, it will not apply any.
        If mentioned users exceed English alphabets, it will start from "A" again
        """
        if name is None:
            name = names.get_first_name()

        if nameType.lower() not in ['alphabet','number']:
            await msg.send(f"Name type {nameType} is unknown, defaulting to number")
            nameType = 'number'
        
        alphabets= list(string.ascii_uppercase)

        if nameType == "number":
            for index, user in enumerate(users):
                await user.edit(nick=f"{name}{index}")

        if nameType == 'alphabet':
            for index,user in enumerate(users):
                if index > len(alphabets):
                    alphabets+=list(string.ascii_uppercase)
                await user.edit(nick=f"{name}{alphabets[index]}")
            
        if name is None:
            for user in users:
                await user.edit(nick=name)
        
        return await msg.send("Nickname changes complete :white_check_mark:")

  


def setup(bot):
    bot.add_cog(Member(bot))
