import asyncio,time,datetime,random,names,pymongo,discord,os
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord.utils import sleep_until





class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    async def timer_completed(self,msg):
        await msg.send(f"Timer complete, {msg.author.mention}")

    @commands.cooldown(rate=2,per=30,type=commands.BucketType.user)
    @command(name='set-timer')
    async def set_timer(self,msg,hours,minutes,seconds):
        """
        Set a timer to do for the bot
        `Ex`: s.set-timer 2 31 23
        `Format`: Hours Minutes Seconds
        `Cooldown`: 30 seconds per command per user
        `Command`: set-timer(hours,minutes,seconds)
        """
        when=datetime.datetime.utcnow() + datetime.timedelta(hours=hours,minutes=minutes,seconds=seconds)
        timer=sleep_until(when,self.timer_completed)
        return await timer(msg)



    @command(aliases=['latency'])
    async def ping(self,msg):
        """
        Check to see how long it's taking for the bot to respond to you
        """
        return await msg.send(f"Pong! 🏓 {round(self.bot.latency,3)}")


    @command(name='wnote',aliases=['take-note','takenote'])
    async def write_note(self,msg,*,note):
        """
        Save the user's note(s) in database for later view
        Possibly for premium users only
        """
        #TODO: check user premium status
        #TODO: Check if current note already exist
            # if TRUE ask to confirm for duplicate note to be added.        
        #TODO: Check user in database
        #TODO: add note length limit per note
        #TODO: add user note database space limit of x

    @command(name='user-noti')
    async def user_notification(self,msg,user:discord.Member):
        """
        Get a notification when the member(s) of your choice is online
        """
        pass

    
    @command(aliases=['remind-me','remindme'])
    async def reminder(self,msg,_time,*,message):
        """
        Remind the user of what 
        """
        pass

    @commands.group()
    @commands.cooldown(rate=2,per=3600,type=commands.BucketType.user)
    async def online_briefing(self,msg):
        """
        Get a briefing of the things you've missed while you were offline 
        """
        #TODO: make it premium or support server joined users only
        if msg.invoked_subcommand is None:
            return msg.send(msg.command.help)
        

    @online_briefing()
    @command()
    async def channel(self,msg):
        """
        See how many messages you've missed 
        How many have messages
        Media formates sent (GIF,images, image links,videos,emotes)
        Last message sent by user
        See latest message sent
        """
        pass


    @online_briefing()
    @command(name='mem-message',aliases=['mem-msgs','memmsgs'])
    async def member_messages(self,msg,user:discord.Member):
        """
        See the amount of messages sent by specific user missed
        see latest message
        see amount of media formates sent by that user  (GIF,images,links,video,emotes)
        See amount of mentions user posted
        See mentioned users?
        amount of channels messages were sent
        amount of times users were mentioned

        """
        pass

    @online_briefing()
    @command(name='role-messages')
    async def role_messages(self,msg,role:discord.Role):
        """
        amount of messaages sent by that role
        amount of times the role was mentioned
        amount of people that mentioned it
        amount of media formats sent by that role
        amount of channels that contain messages with role
        amount of messages sent in each channel with role
        """
        pass
    @online_briefing()
    @command(name='admin-brief',hidden=True,enabled=False)
    async def admin_briefing(self,msg):
        """
        Channels with changes made
        amount of messages deleted by mods
        amount of users that left the server
        """
        pass





def setup(bot):
    bot.add_cog(Utility(bot))

