import discord,time,datetime,asyncio
from discord import file
import requests
from discord.ext.commands import Cog,command
from discord.ext import tasks
import json

class ArcheageEvents(Cog,name="Archeage"):
    def __init__(self,bot):
        self.bot = bot
        self.event_lists=json.loads(open("archeageEvents.json","r").read())
        self.main_time = time.gmtime()
        self.days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        self.channels= {} #Warning times: channel ids {"50":[]}


    def setup_cog(self):
        # start the timer and open JSON even timers 
        try:
            file = open("ArcheageEvents.json","r").read()
        except FileNotFoundError:
            Cog.cog_unload("Archeage")

        new_dict = json.loads(file)
        file.close()

        for exclude in new_dict['Excludes']:
            # Remove all keys inside key "Excludes"
            new_dict.pop(exclude)
        self.event_lists = new_dict
        self.archeage_event_timer.start()


    async def alert_users(self,event,notice_time):
        location= None
        for chan in self.channels:
            if notice_time in self.channels:
                location = self.channels[chan[0]]
                await self.channel.send(f"Event {event} is comming up in {notice_time}")

    @tasks.loop(seconds=5)
    async def archeage_event_timer(self):
        # update time ever x seconds
        # check if an event is nearing start
        self.main_time = time.gmtime()
        day = self.days[self.main_time.tm_wday]
        for key,value in self.event_lists.items():
            for eventDays in value:
                if day == eventDays:
                    for startTime in eventDays:
                        eventHour = startTime[:2]
                        if eventHour[0] == "0":
                            eventHour  = int(eventHour[1:2])
                        else:
                            eventHour = int(eventHour)

                        if (eventHour-self.main_time.tm_hour) == 1:
                            # one hour warning before event
                            minute = int(startTime[3:])
                            if minute > 20:
                                await self.alert_users(key,minute)

                        


                    



    @command(name='utc-now')
    async def utc_now(self,msg):
        # get current UTC time 
        # Hour:Minute
        current_UTC = time.gmtime()
        await msg.send(f"**{current_UTC.tm_hour}:{current_UTC.tm_min}:{current_UTC.tm_sec}**")



    @command()
    async def remind_event(self,msg,evetName):
        pass

