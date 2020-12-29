import discord,time,asyncio
from discord.ext import commands
from discord.ext.commands import errors, converter,command
from ..Utils. util_func import random_color
from discord.ext import tasks
import random

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, map):
        emb = discord.Embed(colour=random_color(), title="Help Commands", description=f"**For a list of command categories** `{self.context.prefix}categories`\n**For help with a specific command** {self.context.prefix}help `Command Name`\n**For a list of commands in a specific categories** `{self.context.prefix}help categories name`**\n\n\n[Invite Bot](https://discordapp.com/oauth2/authorize?client_id=403402614454353941&scope=bot&permissions=8) | [Bot Server](https://discord.gg/xXf8pFr)")
        emb.set_thumbnail(url=self.context.bot.user.avatar_url)
        emb.set_footer(icon_url=self.context.guild.icon_url,text=self.context.guild.name)
        return await self.context.send(embed=emb)


    async def send_command_help(self, command):
        command_doc=command.help
        aliases=f" {self.context.prefix}".join(command.aliases)
        if command.aliases:
            emb=discord.Embed(title=f"{self.context.prefix}{command.name} **|** {self.context.prefix}{aliases}", description=f"{command_doc}",color=random_color())
            # emb.set_footer(text='Help Menu')
            return await self.context.send(embed=emb)


        emb=discord.Embed(description=f"{self.context.prefix}{command.name}\n{command_doc}",color=random_color())
        # emb.set_footer(text='Command Help')
        return await self.context.send(embed=emb)

    async def send_cog_help(self,cog):
        cog_help=[]
        for i in cog.get_commands():
            if i.enabled is True:
                if i.hidden is True and self.context.author.id == 185181025104560128:
                    cog_help.append(f"`{i.name}` - {i.short_doc}")
                if i.hidden is False:
                    cog_help.append(f"`{i.name}` - {i.short_doc}")
        
        names=' \n'.join(cog_help)
        emb=discord.Embed(title=f"**{cog.qualified_name}**",description=names,color=random_color())
        emb.set_thumbnail(url=self.context.guild.icon_url)
        # emb.set_footer(text='Cog Menu')
        return await self.context.send(embed=emb)


class Help(commands.Cog):
    """
    Shows the help command and how to use it 
    """
    def __init__(self, bot):
        self.bot=bot
        self._original_help_command = bot.help_command
        self.cog_docs={
            ""
            }
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self


    @property
    def random_color(self):
        return discord.Color.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))




    @command()
    async def categories(self,msg):
        """
        Shows the list of cogs the bot has
        `Ex:` s.modules
        `Command:` cogs()
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
        
        emb=discord.Embed(description=f"**{self.bot.user.name}'s Command Categories**\n{cogs}",color=random_color())
        return await msg.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))