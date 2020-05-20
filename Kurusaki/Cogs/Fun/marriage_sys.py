import discord,asyncio,time,datetime,pymongo,os,string,random, requests as rq,io
from discord.ext import commands
from discord.ext.commands import Cog,command
from PIL import Image




class Marriage(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.database=pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.marriage=self.database.find_one('marriage')
        self.proposal_codes={}


    async def gen_code(self):
        code=""
        loops=0
        _range=10
        chars=list(string.ascii_letters+string.digits)
        while True:
            for i in range(_range):
                code+=random.choice(chars)

            if code not in self.proposal_codes:
                break
        self.proposal_codes[code]={'time':time.time()+86400}
        return code


    async def clear_codes(self):
        while True:
            for code in self.proposal_codes.copy():
                if time.time() >= self.proposal_codes[code]['time']:
                    self.proposal_codes.pop(code)
            await asyncio.sleep(320)




    @command()
    async def propose(self,msg,user:discord.Member,*,message=None):
        if str(user.id) in self.marriage:
            return await msg.send("You are already married")
        
        if str(user.id) in self.marriage:
            return await msg.send(f"{user.name} is already married")

        if str(user.id) in self.marriage['no_marriage']:
            return await msg.send(f"User {user.name} isn't seeking for anyone at the moment")

        code=await self.gen_code()
        self.proposal_codes[code]['user']=user.id
        emb=discord.Embed(description=f"{msg.author.mention} has proposed to you\nPlease use the code {code} to accept or decline with the command.\n`Ex:`\ns.decline {code}\ns.accept {code}")
        emb.set_thumbnail(url=msg.author.avatar_url)
        if message is not None:
            emb.set_footer(text=message)
        #TODO:Complete
        return await msg.send(embed=emb)
    
    @propose.error
    async def propose_error(self,msg,error):
        if isinstance(error,commands.MissingRequiredArgument):
            return await msg.send("Please mention a user or enter their name to propose")
   
   
   
    @command()
    async def accept(self,msg,*,code):
        if code not in self.proposal_codes:
            return await msg.send(f"Proposal code {code} is not found\nPlease check the case-sensitivity and characters")
        #TODO: COMPLETE


    @command(aliases=['reject'])
    async def decline(self,msg,*,code:str):
        if code not in self.proposal_codes:
            return await msg.send(f"Proposal code {code} is not found\nPlease check the case-sensitivity and characters")

        #TODO: complete


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
