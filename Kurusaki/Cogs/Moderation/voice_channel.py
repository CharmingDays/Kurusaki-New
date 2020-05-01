import discord,asyncio,time,random,datetime,pymongo
from discord.ext import commands
from discord.ext.commands import Cog,command


class VoiceChannel(Cog):
    def __init__(self,bot):
        """
        self.sleep_voice={
            "channel ID": {
                "time":"timer",
                "user":"userId"
            }
                }
        """
        self.bot=bot
        self.sleep_voice={}


    async def sleep_timer(self):
        while True:
            if self.sleep_voice:
                for chan in self.sleep_voice.copy():
                    if time.time() >= self.sleep_voice[chan]['time']:
                        _chan= self.bot.get_channel(chan)
                        if _chan.members:
                            for user in _chan.members:
                                await user.edit(voice_channel=None)
                        

                        self.sleep_voice.pop(chan)
            await asyncio.sleep(10)


    @commands.Cog.listener('on_ready')
    async def voice_ready(self):
        voice_loop=asyncio.wait([self.sleep_timer()])
        await voice_loop


    def sleeper():
        # pylint: disable=no-method-argument
        def predicate(msg):
            if msg.author.voice:
                return 'sleep' in msg.author.voice.channel.name.lower() or msg.author.guild_permissions.manage_channels is True

        return commands.check(predicate)



    @sleeper()
    @command(name='voice-timer',aliases=['sleep-timer','sleep-call'])
    async def voice_timer(self,msg,timer:float, _type='min'):
        #TODO: Needs a check to see if there is already a voice timer for the given channel
        """
        Create a timer that will disconnect all members in a voice channel after the timer
        """
        new_timer=0
        if _type == 'min':
            new_timer+=timer*60
        if _type == 'hour':
            new_timer+=(timer*60) *60
        
        if msg.author.voice:
            if msg.author.voice.channel.id not in self.sleep_voice:
                self.sleep_voice[msg.author.voice.channel.id]={"time":time.time()+new_timer,"user":msg.author.id}
                return await msg.send(f"Voice timer set to {timer} {_type}")

            return await msg.send(f"Already timer in `{msg.author.voice.channel.name}`")

    @voice_timer.error
    async def voice_timer_error(self,msg,error):
        if isinstance(error,commands.CheckFailure):
            if msg.author.voice:
                return await msg.send("Command requires a voice channel name with the word **sleep** in it or manage channels permission required")
            
            return await msg.send("Please join a voice channel")


    def cancel_voice():
    #pylint: disable=no-method-argument
        def predicate(msg):
            if msg.author.voice:
                return 'sleep' in msg.author.voice.channel.name.lower()

        return commands.check(predicate)

    @cancel_voice()
    @command(name='stop-voice-timer',hidden=True,enabled=False)
    async def cancel_voice_timer(self,msg):
        if msg.author.voice.channel.id in self.sleep_voice:
            if self.sleep_voice[msg.author.voice.channel.id]['user'] == msg.author.id:
                self.sleep_voice.pop(msg.author.voice.channel.id)
                return await msg.send("Voice timer cancled")


    


def setup(bot):
    bot.add_cog(VoiceChannel(bot))
