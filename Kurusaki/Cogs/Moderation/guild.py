import discord,asyncio,time,random,names
from discord.ext.commands import command
from discord.ext import commands
from random_words  import RandomWords




class Server(commands.Cog):
    def __init__(self,client):
        self.bot=client


    @command()
    async def guild_info(self,msg):
        pass



    @commands.command()
    @commands.is_owner()
    async def memberall(self, ctx):
        msg = await ctx.send(f"Adding roles to **{ctx.guild.member_count} users**.")
        for user in ctx.guild.members:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name="Member"))
        msg.delete()
        await ctx.send(f"Added roles to **{ctx.guild.member_count}**")
        
    @commands.command(aliases=['sr'])
    async def selfrole(self, ctx, opt, role: discord.Role):
        if ctx.guild.id == 699290035953991741:
            if opt == 'remove' or opt == 'r':
                if role.name == 'dev updates':
                    if not "dev updates" in [x.name for x in ctx.author.roles]:
                        await ctx.send("I can't remove a role that you don't have!")
                    else:
                        await ctx.send(f"Self-Role, **DEV UPDATES**, has been successfully removed from **{ctx.author}**!")
                        await ctx.author.remove_roles(role)    
                        
                else:
                    await ctx.send(f"`{role}` isn't a self-role!")

            if opt == 'add' or opt == 'a':
                if role.name == 'dev updates':
                    await ctx.send(f"Self-Role, **DEV UPDATES**, has been successfully given to **{ctx.author}**!")
                    await ctx.author.add_roles(role)
                else:
                    await ctx.send(f"`{role}` isn't a self-role!")
        else:
            pass





    @command(name='guild-owner',aliases=['guildowner'])
    async def guild_owner(self,msg):
        """
        Get the information of the guild owner
        `Ex:` .guild-owner
        """
        user=msg.guild.get_member(msg.guild.owner_id)
        if user is None:
            logs=self.bot.get_channel(693619264065896551)
            await logs.send(f"Could not get the guild info {msg.guild.name} - {msg.guild.id}\nOwner: {msg.guild.owner_id}")
            return await msg.send("Something went wrong while trying to retreive the guild owner ID")

        return await msg.send(f"The guild owner is {user.name}")



    @command(name='guild-info')
    async def guild_info(self,msg):
        """
        Get information about the guild
        `Ex:` .guild-info
        """




    @commands.has_permissions(manage_roles=True)
    @command()
    async def createrole(self,msg,*,roleName):
        """
        Create a new role for the guild
        `Ex:` .create-role Most Active
        `Permissions:` Manage Roles
        """



    @commands.cooldown(rate=5,per=20,type=commands.BucketType.guild)
    @command(name='member-count',aliases=['members'])
    async def member_count(self,msg):
        """
        Get the guild member count
        `Ex:` .member-count
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



    @commands.has_permissions(manage_channels=True)
    @command(name='create-text')
    async def create_text(self,msg,*,name=None):
        random_name=RandomWords().get_random_words()[0:3]
        if name is None:
            return await msg.guild.create_text_channel(name='-'.join(random_name))
        return await msg.guild.create_text_channel(name=name)


    @command()
    async def guild_rename(self,msg,*,newName):
        pass



    @commands.has_permissions(manage_guild=True)
    @command()
    async def guild_invites(self,msg):
        pass
    

def setup(bot):
    bot.add_cog(Server(bot))
