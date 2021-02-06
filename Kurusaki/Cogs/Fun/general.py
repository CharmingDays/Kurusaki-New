import discord, asyncio, os
from discord.ext import commands
from discord.ext.commands import command, Cog
import random,requests as rq
from requests.api import request



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
        `CMD`: cat()
        `Ex`: s.cat
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
        `CMD`: dog()
        `Ex`: s.dog
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



    @command()
    async def wallpaper(self,msg,width= 1920,length=1080,amts:int = 1):
        #TODO: Testing required
        """
        Get a random wallpaper image
        `CMD`: wallpaper(width:Optional,length:Optional,amounts:Optional)
        `Ex`: s.wallpaper 1920 1080 3
        `NOTE`: amount limit is 3
        """
        url = 'https://picsum.photos/1920/1080'
        request_limit = 0
        if amts > 3:
            amts = 3
            await msg.send(f"Wallpaper amount {amts} exceeds the limit of 3, defaulting it to 3")
        
        images = []
        for i in range(amts):
            data = rq.get(url)
            while data.status_code != 200 and request_limit < 5:
                data = rq.get(url)
                request_limit+=1
            if data.status_code == 200:
                images.append(data.url)

        if not images:
            return await msg.send("Something went wrong while trying to retreive the wallpapers, please try again later.")


        if len(images) < amts:
            await msg.send(f"Something went wrong while trying to get the wallpapers. Could only get {len(images)}")

        message = ""
        for img in images:
            message +=f"{img}\n"


        return await msg.send(message)

    @command()
    async def fox(self,msg,amts:int = 1):
        #TODO: Testing required
        """
        Get a random fox picture
        `CMD`: fox(amounts:Optional)
        `Ex`: s.fox 3
        `NOTE`: amount limit is 3
        """
        url = 'https://randomfox.ca/floof'
        request_limit = 0
        if amts > 3:
            amts = 3
            await msg.send(f"Fox picture amount {amts} exceeds the limit of 3, defaulting it to 3")
        
        images = []
        for i in range(amts):
            data = rq.get(url)
            while data.status_code != 200 and request_limit < 5:
                data = rq.get(url)
                request_limit+=1
            if data.status_code == 200:
                images.append(data.json()['image'])

        if not images:
            return await msg.send("Something went wrong while trying to retreive the fox images, please try again later.")


        if len(images) < amts:
            await msg.send(f"Something went wrong while trying to get the fox images. Could only get {len(images)}")

        message = ""
        for img in images:
            message +=f"{img}\n"


        return await msg.send(message)

    @command()
    async def shiba(self,msg,amts:int = 1):
        #TODO: Testing required
        """
        Get a random shiba picture
        `CMD`: shiba(amounts:Optional)
        `Ex`: s.shiba 3
        `NOTE`: amount limit is 10
        """
        url = f'http://shibe.online/api/shibes?count={amts}&urls=true&httpsUrls=true'
        request_limit = 0
        if amts > 10:
            amts = 10
            await msg.send(f"Shiba picture amount {amts} exceeds the limit of 3, defaulting it to 3")

        data = rq.get(url)
        while data.status_code != 200:
            data = rq.get(url)
        
        images = data.json()

        if not images:
            return await msg.send("Something went wrong while trying to retreive the images, please try again later.")


        if len(images) < amts:
            await msg.send(f"Something went wrong while trying to get the images. Could only get {len(images)}")

        message = ""
        for img in images:
            message +=f"{img}\n"


        return await msg.send(message)



def setup(bot):
    bot.add_cog(FunCommands(bot))