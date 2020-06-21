import discord,asyncio,time,datetime,pymongo,os,string,random, requests as rq,io
from discord.ext import commands
from discord.ext.commands import Cog,command
from discord.ext import tasks
from PIL import Image



class Marriage(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.database=pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.marriage=self.database.find_one('marriage')
        self.proposal_codes={}
        self.clear_codes.start()



    @tasks.loop(hours=1)
    async def clear_codes(self):
        for code in self.proposal_codes.copy():
            if time.time() >= self.proposal_codes[code]['time']:
                self.proposal_codes.pop(code)
            



    async def gen_code(self,author,user):
        code=""
        loops=0
        _range=10
        chars=list(string.ascii_letters+string.digits)
        while True:
            for i in range(_range):
                code+=random.choice(chars)

            if code not in self.proposal_codes:
                break
        self.proposal_codes[code]={'time':time.time()+172800,"author":author,"user":"user"}
        return code


    async def proposal_emb(self,msg,user,code):
        emb=discord.Embed(title='Proposal',description=f"{user.mention}, {msg.author.mention} has proposed you for a virtual marriage")
        emb.add_field(name='Accept',value=f'Type in {msg.prefix}accept {code}')
        emb.add_field(name='Reject',value=f'Type in {msg.prefix}reject {code}')
        emb.set_footer(text="The proposal will expire in 48 hours and a new one will need to be created",icon_url=msg.guild.icon_url)
        return emb


    @command()
    async def propose(self,msg,user:discord.Member):
        """
        Propose a virtual marriage to the mentioned user
        `Ex:` s.propose @User
        `
        """
        if str(msg.author.id) in self.marriage:
            partner=self.bot.get_user(self.marriage[str(msg.author.id)]["couple"])
            if partner:
                return await msg.send(f"You are already married to {partner}")
            
            return await msg.send(f"You are already married")

        if str(user.id) in self.marriage:
            partner=self.bot.get_user(self.marriage[str(user.id)]["couple"])
            return await msg.send(f"{user.name} is already married to {partner.name}")

        if user.id in self.marriage['no_marriage']:
            return await msg.send(f"{user.name} does not want to marry anyone at the moment")
        
        code=await self.gen_code(msg.author.id,user.id)
        self.marriage_codes[code]
        message=await self.proposal_emb(msg,user,code)
        return await msg.send(embed=message)

    @propose.error
    async def propose_error(self,msg):
        pass



    async def accept_emb(self,msg,code):
        author=self.bot.get_user(self.proposal_codes[code]['author'])
        emb=discord.Embed(title=f"Congratulations",description=f"Congratulations to {msg.author.mention} {author.mention} for becoming a new couple!")
        emb.set_thumbnail(url="") #NOTE: picture of both author and user
        return emb

    
    @command()
    async def accept(self,msg,code):
        #NOTE: check to see if the person is already married from previous other proposals
        if code in self.proposal_codes and msg.author.id in self.proposal_codes[code]["user"]:
            emb=await self.accept_emb(msg,code)
            self.proposal_codes.pop(code)
            return await msg.send(embed=emb)

        return await msg.send("Sorry, the accept code doesn't exist\nPlease check your spelling and case sensitivity")


    async def make_image(self,msg,user):
        raw_img1=rq.get(msg.author.avatar_url).content
        img1=Image.open(io.BytesIO(raw_img1))
        raw_img=rq.get(user.avatar_url).content
        img=Image.open(io.BytesIO(raw_img))
        new = Image.new('RGB', (img.width + img.width, img.height+img.height))
        new.paste(img1, (0+40, img1.height//2))
        new.paste(img, (img.width, img.height//2))
        resize=new.resize(size=(359,359))
        crop_size=(50,56,339,320)
        cropped=resize.crop(crop_size)
        final=cropped.resize(size=(359,359))
        





def setup(bot):
    bot.add_cog(Marriage(bot))


