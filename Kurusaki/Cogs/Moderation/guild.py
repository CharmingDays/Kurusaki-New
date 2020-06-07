import discord,asyncio,time,random,names
from discord.ext.commands import command
from discord.ext import commands
from random_words  import RandomWords




class Server(commands.Cog):
    def __init__(self,client):
        self.bot=client



    @command(name='guild-info')
    async def guild_info(self,msg):
        """
        Get information about the guild
        `Ex:` .guild-info
        """


    @commands.has_permissions(manage_guild=True)
    @command()
    async def new_icon(self,msg,*,url):
        pass



    @command()
    async def boosters(self,msg):
        """
        Get the list of the current server boosters
        `Ex:` .boosters
        """


    @commands.has_permissions(manage_guild=True)
    @command(name='server-rename')
    async def guild_rename(self,msg,*,newName):
        """
        Change the name of the server
        `Ex:` s.server-rename Valorant Gamers
        `Permissions:` Manage Guild
        `Command:` server-rename(new-name)
        """
        await msg.guild.edit(name=newName,reason=f'Server name changed by {msg.author.name} ({msg.author.id})')
        return await msg.message.add_reaction(emoji='✅')



    @commands.has_permissions(manage_guild=True)
    @command(name='AFK-Chan',aliases=['AFK-Voice'])
    async def AFK_Channel(self,msg,*,channelName:discord.VoiceChannel):
        """
        Make a voice channel into an AFK Voice channel
        `Ex:` s.AFK-Chan AFK People (Will attempt to find voice channel with "exact" name:case sensitive)
        `Permissions:` Manage Guild
        `Command:` AFK-Chan(channel-name:required)
        """
        await msg.guild.edit(afk_timeout=900,afk_channel=channelName,reason=f'AFK channel command used by {msg.author.name} ({msg.author.id})')
        await msg.message.add_reaction(emoji='✅')
        return await msg.send(f"Members will now be moved to {channelName} after being AFK for 15 minutes or more.")



    @commands.has_permissions(manage_guild=True)
    @command(name='afk-timeout')
    async def afk_timeout(self,msg,timer:int=900):
        """
        Change the AFK timeout timer for the server value of seconds
        `Ex:` s.afk-timeout 1200 (Sets timer to 1200 (20 min) seconds for moving member to afk channel)
        `Note:` entered values must be an "integer"
        `Permissions:` Manage Guild
        `Command:` afk-timeout(timer:required)
        """
        try:
            int(timer)
        except:
            return await msg.send("Please enter an integer.")
        
        await msg.guild.edit(afk_timeout=timer)
        return await msg.send(f"AFK timeout set to {timer/60} minutes.")



    @commands.has_permissions(manage_guild=True)
    @command()
    async def guild_invites(self,msg):
        pass
    
    
    @commands.has_permissions(manage_roles=True)
    @command(name='create-role',aliases=['make-role','new-role'],enabled=False)
    async def create_role(self,msg,*,roleName:discord.Role):
        """
        Create a new in the server
        `Ex:` s.create-role Support Players
        `Permissions:` Manage Roles
        `Command:` create-role(role-name:required)
        """
        role=await msg.guild.create_role(name=roleName,reason=f'New role created by {msg.author.name} ({msg.author.id})')
        return await msg.send(f"New role {role.name} has been created")
        #TODO: make it so that it can manage permissions for the role via reactions of the role in embeds


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

    @commands.has_permissions(ban_members=True)
    @command()
    async def unban(self,msg,user:int):
        try:
            int(user)
        except:
            return await msg.send("Please enter the user's ID")
            
        user_obj=self.bot.get_user(user)
        await msg.guild.unban(user=user_obj,reason=f"User unbanned by {msg.author.name} ({msg.author.id})")
        await msg.send(f"{msg.author.name} has unbanned {user_obj.name}")


def setup(bot):
    bot.add_cog(Server(bot))
