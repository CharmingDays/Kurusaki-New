import discord,time,asyncio
from discord.ext import commands
from discord.ext.commands import errors, converter,command
import subprocess
from discord.ext import tasks
import random

class MyHelpCommand(commands.MinimalHelpCommand):
    def random_color(self):
        return random.randint(1,255)


    async def send_bot_help(self, map):
        emb = discord.Embed(colour=discord.Color.from_rgb(self.random_color(),self.random_color(),self.random_color()), title="Help Commands", description=f"**For a list of modules** `{self.context.prefix}modules`\n**For help with a specific command** {self.context.prefix}help <Command Name>\n**For a list of all commands in a specific module** `{self.context.prefix}help` <Module Name>\n\n\n[Invite Me](https://discordapp.com/oauth2/authorize?client_id=403402614454353941&scope=bot&permissions=8) | [Support Server](https://discord.gg/XVTex62)")
        emb.set_thumbnail(url=self.context.bot.user.avatar_url)
        emb.set_footer(icon_url=self.context.guild.icon_url,text=self.context.guild.name)
        return await self.context.send(embed=emb)

    async def send_command_help(self, command):
        command_doc=command.help
        aliases=f" {self.context.prefix}".join(command.aliases)
        if command.aliases:
            emb=discord.Embed(title=f"{self.context.prefix}{command.name} **|** {self.context.prefix}{aliases}", description=f"{command_doc}",color=discord.Color.from_rgb(self.random_color(),self.random_color(),self.random_color()))
            emb.set_footer(text='Command Help')
            return await self.context.send(embed=emb)


        emb=discord.Embed(description=f"{self.context.prefix}{command.name}\n{command_doc}",color=discord.Color.from_rgb(self.random_color(),self.random_color(),self.random_color()))
        emb.set_footer(text='Command Help')
        return await self.context.send(embed=emb)

    async def send_cog_help(self,cog):
        cog_help=[]
        # emb1=discord.Embed(title=f"**{cog.qualified_name}**",color=discord.Color.from_rgb(self.random_color(),self.random_color(),self.random_color()))
        # emb1.set_thumbnail(url=self.context.guild.icon_url)
        for i in cog.get_commands():
            if i.hidden is not True and i.enabled is not False:
                cog_help.append(f"`{i.name}` - {i.short_doc}")
                # emb1.add_field(name=f"**{i.name}**",value=f"{i.short_doc}",inline=True)
        
        names=' \n'.join(cog_help)
        emb=discord.Embed(title=f"**{cog.qualified_name}**",description=names,color=discord.Color.from_rgb(self.random_color(),self.random_color(),self.random_color()))
        emb.set_thumbnail(url=self.context.guild.icon_url)
        # await self.context.send(embed=emb1)
        return await self.context.send(embed=emb)





class Help(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self._original_help_command = bot.help_command
        self.cog_docs={
            ""
            }
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self


    @command()
    async def modules(self,msg):
        """
        Shows the list od modules the bot has
        `Ex:` s.modules
        `Command:` modules()
        """

        cogs=""
        cog_dict=self.bot.cogs
        for cog in self.bot.cogs:
            if cog.lower() == 'nsfw' and msg.guild.id == 264445053596991498:
                pass
            
            if cog.lower() == 'events':
                pass

            else:
                cogs+=f"`{cog}` - {cog_dict[cog].description}\n"
        
        emb=discord.Embed(description=f"**{self.bot.user.name}'s Modules**\n{cogs}")
        return await msg.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))