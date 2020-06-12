import discord,time,random,names
import requests as rq
import asyncio
import typing
import logging
from discord.ext.commands import command
from discord.ext import commands


class Server(commands.Cog):
    """
    Server related commands to easily manage your server
    """
    def __init__(self,client):
        self.bot=client


    def random_color(self):
        return random.randint(1,255)

    @commands.guild_only()
    @commands.cooldown(type=commands.BucketType.channel,rate=1,per=3)
    @command(name='server-info')
    async def guild_info(self,msg):
        """
        Get information about the guild
        `Ex:` s.server-info
        `Command:` server-info()
        """
        emotes=""
        for emote in msg.guild.emojis:
            emotes+=f"<:{emote.name}:{emote.id}>"
        emb=discord.Embed(title=f"{msg.guild.name} - {msg.guild.id}",description=msg.guild.description,color=discord.Color.from_rgb(self.random_color(),self.random_color(),self.random_color()))
        emb.set_thumbnail(url=msg.guild.icon_url)
        emb.add_field(name="Created Date",value=f"{msg.guild.created_at} UTC")
        emb.add_field(name='AFK Channel',value=msg.guild.afk_channel)
        emb.add_field(name="AFK Timer",value=f"{str(msg.guild.afk_timeout/60)[:4]} Minutes")
        emb.add_field(name="Owner",value=msg.guild.owner.mention)
        emb.add_field(name="Members",value=len(msg.guild.members))
        if msg.guild.text_channels:
            emb.add_field(name="Text Channels",value=len(msg.guild.text_channels))
        if not msg.guild.text_channels:
            emb.add_field(name="Text Channels",value=None)
        if msg.guild.voice_channels:
            emb.add_field(name="Voice Channels",value=len(msg.guild.voice_channels))
        
        if not msg.guild.text_channels:
            emb.add_field(name="Voice Channels",value=None)

        if msg.guild.categories:
            emb.add_field(name="Categories",value=len(msg.guild.categories))
        if not msg.guild.categories:
            emb.add_field(name="Categories",value=None)

        if msg.guild.roles:
            emb.add_field(name="Roles",value=len(msg.guild.roles))
        if not msg.guild.roles:
            emb.add_field(name="Roles",value=None)

        if msg.guild.emojis:
            emb.add_field(name=f'{len(msg.guild.emojis)} Emojis',value=emotes)
        if not msg.guild.emojis:
            emb.add_field(name=f'Emojis',value=None)

        await msg.send(embed=emb)

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @command(name='new-icon')
    async def new_icon(self,msg,*,url=None):
        """
        Change the icon of the the server (Only PNG/JPEG supported, and GIF if availale to server)
        `Ex:` s.new-icon https://i.pinimg.com/originals/7c/46/44/7c4644a00c5c1e46dda0d9263bf6cf62.jpg (Or upload an image)
        """
        if url is None:
            if msg.message.attachments:
                try:
                    image=rq.get(msg.message.attachments.url).content
                    await msg.guild.edit(icon=image)
                    return await msg.send(f"New server icon set to {msg.message.attachments}")
                except Exception as Error:
                    await msg.send("Bot was unable to set provided image as server icon")

            return msg.send("Please upload an image to change the icon paste a url after command")

        if url is not None:
            try:
                image=rq.get(url).content
                await msg.guild.edit(icon=image,reason=f"Server icon changed by {msg.author.name} ({msg.author.id})")
                return await msg.send(f"New icon set to {url}")
            except Exception as Error:
                return await msg.send("Could not use the provided image link as server icon")


        
    @commands.guild_only()
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



    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @command(name='afk-chan',aliases=['afk-voice'])
    async def AFK_Channel(self,msg,*,channelName:discord.VoiceChannel):
        """
        Make a voice channel into an AFK Voice channel and it's timer
        `Ex:` s.afk-chan AFK-Voice-Channel (Will attempt to find voice channel with "exact" name:case sensitive)
        `Permissions:` Manage Guild
        `Command:` AFK-Chan(channel-name:required)
        """
        await msg.guild.edit(afk_channel=channelName,reason=f'AFK channel command used by {msg.author.name} ({msg.author.id})')
        await msg.message.add_reaction(emoji='✅')
        return await msg.send(f"Members will now be moved to {channelName} after being AFK for 15 minutes or more.")

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @command(name='afk-timer')
    async def afk_timer(self,msg,timer:typing.Optional[int]=300):
        """
        Change the AFK voice timer in seconds
        `Ex:` s.afk-timer 449
        `Permissions:` Manage Guild
        `Command:` afk-timer(time:integer|optional)
        """
        new_time=str(timer/60)
        await msg.guild.edit(afk_timeout=timer,reason=f"AFK timer changed by {msg.author.name} ({msg.author.id})")
        return await msg.send(f"AFK timer changed to {new_time[:3]}")

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @command()
    async def invites(self,msg):
        codes=await msg.guild.invites()
        
        if codes:
            return await msg.send("`{}`".format(' \ndiscord.gg/'.join(codes)))

        return await msg.send("No current active invites found.")
    
    @commands.guild_only()    
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


    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @command(enabled=False)
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


def setup(bot):
    bot.add_cog(Server(bot))
