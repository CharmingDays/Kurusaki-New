import discord,time,asyncio
from discord.ext import commands
from discord.ext.commands import errors, converter,command
import subprocess
from discord.ext import tasks

class MyHelpCommand(commands.MinimalHelpCommand):

    async def send_bot_help(self, map):
        embed = discord.Embed(colour=0x7ED321, title="Useful help commands", description=f"**For a list of modules** `{self.context.prefix}modules`\n**For help with a specific command** {self.context.prefix}help <Command Name>\n**For a list of all commands in a specific module**{self.context.prefix}help <Module Name>\n\n\n[Invite Me](https://discordapp.com/oauth2/authorize?client_id=683098157877297178&scope=bot&permissions=66186303) | [Support Server](https://discord.gg/jDFrFQC)")
        embed.set_thumbnail(url=self.context.bot.user.avatar_url)
        return await self.context.send(embed=embed)

    async def send_command_help(self, command):
        command_doc=command.help
        aliases=f" {self.context.prefix}".join(command.aliases)
        if command.aliases:
            emb=discord.Embed(title=f"{self.context.prefix}{command.name} **/** {self.context.prefix}{aliases}", description=f"{command_doc}",color=0x7ED321)
            emb.set_footer(text='Command Help')
            return await self.context.send(embed=emb)


        emb=discord.Embed(description=f"{self.context.prefix}{command.name}\n{command_doc}",color=0x7ED321)
        emb.set_footer(text='Command Help')
        return await self.context.send(embed=emb)

    async def send_cog_help(self,cog):
        cog_help=[]
        for i in cog.get_commands():
            if i.hidden is not True and i.enabled is not False:
                cog_help.append(f"`{i.name}` - {i.short_doc}")
        
        names=' \n'.join(cog_help)
        emb=discord.Embed(title=f"**{cog.qualified_name}**\n{names}")
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
        cogs=""
        for cog in self.bot.cogs:
            if cog.lower() == 'botowners' and msg.author.id not in [185181025104560128,648625673912713217]:
                pass
            if cog.lower() == 'nsfw' and msg.guild.id == 264445053596991498:
                pass
            
            if cog.lower() == 'events':
                pass

            else:
                cogs+=f"`{cog}`\n"
        
        emb=discord.Embed(description=f"**{self.bot.user.name}'s Modules**\n{cogs}")
        return await msg.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))