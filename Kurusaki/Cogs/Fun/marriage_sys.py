import discord,asyncio,time,datetime,pymongo,os,string,random, requests as rq,io
from discord.ext import commands
from discord.ext.commands import Cog,command
from PIL import Image




class Marriage(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.database=pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.marriage=self.database.find_one('marriage')
        self.proposal_ids={}
        self.proposals={"users":[]}
        self.__proposal_ids__={
            "jf23fj":{"time":time.time(),"id":94839483984}
        }
        self.channels={
            "logs":682513406682857540,
            'temp-pic':700595769551487106
        }





    async def delete_proposal_ids(self):
        while True:
            for ids in self.proposal_ids.copy():
                if time.time() > self.proposal_ids[ids]['time']:
                    self.proposal_ids.pop(ids)
                    

            await asyncio.sleep(900)





    async def gen_marriage_id(self):
        chars=list(string.digits+string.ascii_letters)
        tries=0
        _range=7
        _id=''
        while True:
            for i in range(random.randint(5,_range)):
                _id+=random.choice(chars)
            if _id not in self.proposal_ids:
                self.proposal_ids[_id]=time.time()+172800
                return _id
            tries+=1

            if tries//2 > 4:
                _range+=1



    @commands.guild_only()
    @command()
    async def propose(self,msg,user:discord.Member):
        if msg.author.id in self.proposals['users']:
            return await msg.send("Please wait until your previous proposal code has expired")
        

        if msg.author.id == user.id:
            chan=self.bot.get_channel(self.channels['logs'])
            await chan.send(f"{msg.author} has attempted to do self-marriage")
            return await msg.send("Self marriage is currently not supported yet.\nPlease stay tuned for this feature.")
        


        if msg.author.id in self.marriage['married']:
            return await msg.send("You are already married")


        if user.id in self.marriage['married']:
            return await msg.send(f"{user.name} is already married")
        
        if user.id in self.marriage['no_marriage']:
            return await msg.send(f"{user.name} wishes not to marry anyone at the moment")
        

        accept_id=await self.gen_marriage_id()
        self.proposals['users'].append(msg.author.id)
        self.proposals[accept_id]=msg.author.id
        emb=discord.Embed(description=f'{msg.author.mention} has proposed to you {user.mention}\nUse the command {msg.prefix}accept or {msg.prefix}decline with the code {accept_id}\n`Ex:` {msg.prefix}accept {accept_id}\n`Ex:` {msg.prefix}decline {accept_id}')
        emb.set_thumbnail(url=msg.author.avatar_url)
        emb.set_footer(text='The proposal code will expire in 48 hours')
        await msg.send(embed=emb)

    @propose.error
    async def propose_error(self,msg,error):
        if isinstance(error,commands.CheckFailure):
            await msg.author.send("This command can only be used inside a server.")





    @command()
    async def decline(self,msg,*,Id):
        if Id not in self.proposals:
            return await msg.send("Proposal ID not found, please check to make sure you enterted the ID correctly.\nCharacters are case-sensitive.`Ex:` **HeLlO** and **Hello** are not the same.")
        
        if Id in self.proposals:
            user=self.bot.get_user(self.proposals[Id])
            if Id in self.proposal_ids:
                self.proposal_ids.pop(Id)
            self.proposals.pop(Id)

            return await user.send(f"Unfortunately {msg.author} has declined your proposal. Better luck next time.")



    @command()
    async def accept(self,msg,*,Id):
        if Id not in self.proposals:
            return await msg.send("Proposal ID not found, please check to make sure you enterted the ID correctly.\nCharacters are case-sensitive.`Ex:` **HeLlO** and **Hello** are not the same.")

        if Id in self.proposals:
            user=self.bot.get_user(self.proposals[Id])
            if Id in self.proposal_ids:
                self.proposal_ids.pop(Id)
            self.proposals.pop(Id)
            self.marriage['married'].append(user.id)
            self.marriage['married'].append(user.id)
            self.marriage[str(user.id)]={"date":datetime.datetime.now().utcnow(),"time":time.time(),"couple":msg.author.id}
            self.marriage[str(msg.author.id)]={"date":datetime.datetime.now().utcnow(),"time":time.time(),"couple":user.id}
            self.database.update_one({'_id':'marriage'},{'$set':self.marriage})
            await msg.send(f"{msg.author} has accepted your proposal!")
            return await msg.send("Congratulations for {} and {} for becoming a couple!")



    @command()
    async def divorce(self,msg):
        pass



    @command(aliases=['marriage-info'])
    async def anniversary(self,msg):
        if str(msg.author.id) not in self.marriage:
            return await msg.send("You are currently do not have a couple yet.")

        if str(msg.author.id) in self.marriage:
            chan=self.bot.get_channel(self.channels['temp-pic'])
            user=self.bot.get_user(self.marriage[str(msg.author.id)]['couple'])

            def make_img():
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
                

            date=self.marriage[str(msg.author.id)]['date']
            timestamp=self.marriage[str(msg.author.id)]['time']
            emb=discord.Embed(title='Anniversary')
            # emb.set_image(url=msg.author.avatar_url)
            emb.set_thumbnail(url=user.avatar_url)
            emb.add_field(name='Date',value=f"**{date}** UTC")
            emb.add_field(name='Timestamp',value=f"**{timestamp}**")
            emb.set_footer(text=f'{msg.guild.name}',icon_url=msg.guild.icon_url)
            return await msg.send(embed=emb)



def setup(bot):
    bot.add_cog(Marriage(bot))
