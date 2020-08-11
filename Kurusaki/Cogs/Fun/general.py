import discord, asyncio, os
from discord.ext import commands
from discord.ext.commands import command, Cog
import random,requests as rq



class FunCommands(Cog,name='Fun Commands'):
    """
    A series of commands for your entertainment
    """
    def __init__(self,bot):
        self.bot=bot

    #TODO:LIST OF COMMANDS TO CREATE BELOW
    #neko, anime commands, movie commands, facts command, joke command, random name command, random commands

    @property
    def random_color(self):
        """
        Return a random discord embed color
        """
        return discord.Color.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))


    @command(name='8ball')
    async def _8ball(self,msg,*,question=None):
        """
        Ask the magical 8 ball your question
        `Ex`: s.8ball Will I become famous?
        `Command`: 8ball(queestion)
        """
        if question is None:
            return await msg.send("Please input a question to ask the 8ball")
        ball_answers=['The magical 8 ball said, No','The magical 8 ball said, Yes','The magical 8 ball said, Maybe','8 ball said, Yes','8 ball said, No','8 ball said, Maybe','Yes','No','Maybe','Maybe 🤔']
        return await msg.send(ball_answers)


    @command()
    async def fox(self,msg):
        """
        Get a picture of a real life fox
        `Ex`: s.fox
        `Command`: fox()
        """
        data=rq.get('https://randomfox.ca/floof/')
        emb=discord.Embed(color=self.random_color)
        if data.ok:
            emb.set_image(url=data.json()['image'])

        else:
            emb.set_image(url=f'https://http.cat/{data.status_code}')
            emb.set_footer(text='something went wrong. D:')

        return await msg.send(embed=emb)


    @command()
    async def cat(self,msg):
        """
        Get a picture of a random cat to make your day a little better
        `Ex`: s.cat
        `Command`: cat()
        """
        api_key=os.getenv('CAT_API_KEY')
        cat=rq.get(f'https://api.thecatapi.com/v1/images/search?limit=1&page=1&api_key={api_key}')
        emb=discord.Embed(color=self.random_color)
        if cat.ok:
            emb.set_image(url=cat.json()['url'])
        
        else:
            emb.set_image(url=f'https://http.cat/{cat.status_code}')
            emb.set_footer(text='Something went wrong. D:')

        return await msg.send(embed=emb)


    @command()
    async def dog(self,msg):
        """
        Get a picture of a random dog to make your day a little better
        `Ex`: s.dog
        `Command`: dog()
        """
        #NOTE:Alternative dog images
        #http://shibe.online/api/shibes?count=1&urls=true
        dog=rq.get('https://random.dog/woof.json')
        emb=discord.Embed(color=self.random_color)
        if dog.ok:
            emb.set_image(url=dog.json()['url'])
        
        else:
            emb.set_image(url=f'https://http.cat/{dog.status_code}')
            emb.set_footer(text='Something went wrong. D:')

        return await msg.send(embed=emb)





def setup(bot):
    bot.add_cog(FunCommands(bot))
