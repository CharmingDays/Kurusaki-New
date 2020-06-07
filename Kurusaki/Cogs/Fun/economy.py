import discord,asyncio,time,datetime,random,typing,pymongo,os,json
from discord.ext import commands
from discord.ext.commands import Cog,command


class Economy(Cog):
    def __init__(self,bot):
        self.bot=bot
        bot.loop.create_task(self.background_events())
        self.EconData = pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['Economy']
        self.data=self.EconData.find_one("global_econ")
        self.data_counter=0
        self.in_voice=[]
        self.shop=['status-change','Role?']
        self.logs={
            'econ':693619264065896551
        }

         
    async def update_database(self):
        new_data=self.EconData.find_one('global_econ')
        if self.EconData != new_data:
            self.EconData.update_one({'_id':'global_econ'},{'$set':self.data})


    async def voice_econ(self):
        while True:
            for user in self.in_voice:
                if user in self.data:
                    self.data[user]+=1
            self.data_counter+=len(self.in_voice)
            await asyncio.sleep(120)


    async def background_events(self):
        await self.bot.wait_until_ready()
        self.bot.loop.create_task(self.voice_econ())


    @Cog.listener('on_voice_state_update')
    async def voice_passive_income(self,user,before,after):
        """
        Make it so that users can gain passive income from being inside a voice channel
        """
        if user.bot == True:
            return 

        if str(user.id) not in self.data:
            self.data[str(user.id)]=5

        if after.channel is not None:
            if user.id not in self.in_voice:
                self.in_voice.append(str(user.id))
            #User joins voice

        if after.channel is None:
            #User leaves voice
            if user.id in self.in_voice:
                self.in_voice.remove(str(user.id))


    
    async def clear_user(self,userId):
        self.data.pop(str(userId))


    @Cog.listener("on_message")
    async def income_cal(self,msg):
        if msg.author.id in self.data['econ_off']:
            return None
        
        if msg.author.bot is True:
            return None
        
        if str(msg.author.id) in self.data:
            if len(msg.content) <=5:
                self.data[str(msg.author.id)]+=1
                self.data_counter+=1
                return 

            if len(msg.content) <=20 and len(msg.content) >5:
                self.data[str(msg.author.id)]+=6
                self.data_counter+=1
                return 

            if len(msg.content) <=50 and len(msg.content) >20:
                self.data[str(msg.author.id)]+=10
                self.data_counter+=1
                return 

            if len(msg.content) >=100 and len(msg.content) >50:
                self.data[str(msg.author.id)]+=15
                self.data_counter+=1
                return 

            if self.data_counter >= 1000:
                #NOTE: THIS WILL LATER BE CHANGED INTO A TIMER WHEN MORE USERS ARE PRESENTLY USING THIS FEATURE
                return await self.update_database()
     
        elif msg.author.bot == False and str(msg.author.id) not in self.data:
            self.data[str(msg.author.id)]=5
            return


    @command(name='econ-on',aliases=['activate-econ','activateEcon','econon'])
    async def activate_econ(self,msg):
        """
        Turn back economy mode back on and restart the grind.
        `Ex:` .econ-on
        """
        if msg.author.id in self.data['econ_off']:
            self.data['econ_off'].remove(msg.author.id)
            return await msg.message.add_reaction(emoji='✅')

        return await msg.send("You are already have economy mode activated.")


    @command(name='econ-off',aliases=['EconOff'])
    async def econ_off(self,msg):
        """
        Turn off economy mode and delete your data.
        `Ex:` .econ-off
        """
        if str(msg.author.id) in self.data:
            self.data.pop(str(msg.author.id))
            self.data['econ_off'].append(msg.author.id)
            return await msg.send("You have been removed from the economy mode and your data has been deleted")
        
        else:
            return await msg.send("You are not in econ mode")


    @command(aliases=['leaderboards','lb'])
    async def rank(self,msg,amts:int=10):
        """
        View the current leaderboard for the economy.
        `Ex:` .rank
        """
        if amts > 100:
            amts = 90
            await msg.send(f"Can't view above {amts} yet")
        remove_user=[]
        leads=[]
        new_data=self.data.copy()
        new_data.pop('_id')
        new_data.pop('econ_off')
        for userData in sorted(new_data.items(),key=lambda x: x[1],reverse=True):
            if self.bot.get_user(int(userData[0])) is None:
                remove_user.append(userData[0])

            else:
                leads.append([self.bot.get_user(int(userData[0])),userData[1]])

        data_format=""
        for index,user in enumerate(leads):
            if index >= amts:
                break
            data="{}: {} - {}\n"
            data_format+=data.format(index+1,user[0].name,user[1])
        
        return await msg.send(f"```yaml\n{data_format}\n```")



    @command(aliases=['item-shop','itemshop'],hidden=True,enabled=False)
    async def shop(self,msg,page=1):
        """
        See the list of items that are avaliable to buy with the currency
        `Ex:` .shop
        """
        emb=discord.Embed(description=f'**Shop**\nChange bot status')



    @command(aliases=['buy-item','get-item','buyitem','getitem'],enabled=True,hidden=True)
    async def buy_item(self,msg,*,itemName):
        if itemName in self.shop:
            pass


        return await msg.send(f"Item {itemName} not found.")
    



    @commands.cooldown(rate=2,per=10,type=commands.BucketType.user)
    @command(aliases=['user-rank'])
    async def coin(self,msg,user:discord.Member=None):
        if user is None:
            return await msg.send("**Please mention a user to check the currency**")
        
        if str(user.id) not in self.data:
            return await msg.send("User has no coins")
        
        if str(user.id) in self.data:
            return await msg.send(f"```yaml\n{self.bot.get_user(user.id).name} - {self.data[str(user.id)]}```")
        
        return await msg.send("Something went wrong D:")



    @commands.cooldown(rate=7,per=86400,type=commands.BucketType.user)
    @command(aliases=['gift'])
    async def give(self,msg,points,*users:discord.Member):
        """
        Give some of your currency to mentioned member(s)
        `Ex:` .gift 200 @User1 @User2
        `Note:` 200 will be given to both users
        """
        unable_user=[]
        if str(msg.author.id) not in self.data and points > 5:
            return await msg.send("You do not have enough to gift anyone")

        if users:
            if len(users)*points > self.data[str(msg.author.id)]:
                return await msg.send(f"Not enough points to gift {' '.join([user.name for user in users])}")

            for user in users:
                if user.id not in self.data['econ_off']:
                    if str(user.id) not in self.data:
                        self.data[str(user.id)]=points

                    else:
                        self.data[str(user.id)]+=points

                else:
                    unable_user.append(user.name)
            if unable_user:
                self.data[str(msg.author.id)]-=points*(len(users)-len(unable_user))
                await msg.send(f"Unable to gift {' '.join(unable_user)} because they have economy mode off")
            
            else:
                self.data[str(msg.author.id)]-=points*len(users)


            return await msg.message.add_reaction(emoji='✅')
            
        return await msg.send("Please mention the user(s) you'd like to gift")



    @commands.is_owner()
    @command(hidden=True,name='econ-update')
    async def admin_update_econ(self,msg):
        """
        Trigger the update of the economy database to mongoDB
        .admin-econ-update
        """
        new_data=self.EconData.find_one('global_econ')
        if new_data != self.data:
            self.EconData.update_one({'_id':'global_econ'},{'$set':self.data})
            self.data_counter=0
            return await msg.message.add_reaction(emoji='✅')

        
        return await msg.send("No new changes in database to update")


    @admin_update_econ.error
    async def admin_error(self,msg,error):
        if isinstance(error,commands.CheckFailure):
            chan=self.bot.get_channel(690340608019398927)
            return await chan.send(f'User {msg.author} ({msg.author.id}) attempted to use an admin command only bot owner can use.')

        return error


def setup(bot):
    bot.add_cog(Economy(bot))
