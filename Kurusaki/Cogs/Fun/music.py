import discord,asyncio,time,datetime,names,random,pymongo,youtube_dl,string,os,functools,json
from discord.ext import commands
from discord.ext.commands import command



#TODO: CREATE PLAYLIST SUPPORT FOR MUSIC



#flat-playlist:True?
#|
#|
#extract_flat:True
ytdl_format_options= {
    'format': 'bestaudio/best',
    'outtmpl': '{}',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    "extractaudio":True,

    "audioformat":"opus",
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

stim= {
    'default_search': 'auto',
    "ignoreerrors":True,
    'quiet': True,
    "no_warnings": True,
    "simulate": True,  # do not keep the video files
    "nooverwrites": True,
    "keepvideo": False,
    "noplaylist": True,
    "skip_download": False,
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}


ffmpeg_options = {
    'options': '-vn'
}

class Downloader(discord.PCMVolumeTransformer):
    def __init__(self,source,*,data,volume=0.6):
        super().__init__(source,volume)
        self.data=data
        self.title=data.get('title')
        self.url=data.get("url")
        self.thumbnail=data.get('thumbnail')
        self.duration=data.get('duration')
        self.views=data.get('view_count')
        self.yt_token=None
        self.set_ytAPI()
        self.playlist={}


    def set_ytAPI(self):
        try:
            token=os.environ['YOUTUBE_API']
            self.yt_token=token
        except KeyError:
            pass


    @classmethod
    async def video_url(cls,url,ytdl,*,loop=None,stream=False):
        loop=loop or asyncio.get_event_loop()
        data= await loop.run_in_executor(None,lambda: ytdl.extract_info(url,download=not stream))
        data1={'queue':[]}
        if 'entries' in data:
            if len(data['entries']) >1:
                playlist_titles=[title['title'] for title in data['entries']]
                data1={'title':data['title'],'queue':playlist_titles}
                data1['queue'].pop(0)

            data=data['entries'][0]
                
        filename=data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename,**ffmpeg_options),data=data),data1



    async def get_info(self,url):
        yt=youtube_dl.YoutubeDL(stim)
        down=yt.extract_info(url,download=False)
        data1={'queue':[]}
        with open('files.json','w',encoding='utf-8') as f:
            f.write(json.dumps(down))
        if 'entries' in down:
            if len(down['entries']) > 1:
                playlist_titles=[title['title'] for title in down['entries']]
                data1={'title':down['title'],'queue':playlist_titles}

            down=down['entries'][0]['title']
            
        return down,data1

        # url='https://www.youtube.com/playlist?list=PLl0zPB9P7QsIL19qIbmrWF4MHJoMoHng7'        
        # url2="https://www.youtube.com/watch?v=NbSnecTTRSA&list=PLl0zPB9P7QsIL19qIbmrWF4MHJoMoHng7&index=2&t=0s"
        # url3='https://www.youtube.com/{playlist}?{list}={playlist_ID}'



class MusicPlayer(commands.Cog,name='Music'):
    def __init__(self,client):
        self.bot=client
        self.database = pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        self.music=self.database.find_one('music')
        self.player={
            "audio_files":[]
        }
        self.__player__={
            "audio_files":[],
            "guildId: int":{
                "player":'player object', #NOTE: get current songs from player
                'queue':[{'title':'the sound of silence','author':'`user object`'},{'title':"Hello - Adel",'author':'`user object`'}],
                'play':'True or False',
                'name':'current audio file name',
                'author':'user obj',
                'repeat':False
            }
        }

    @commands.Cog.listener('on_voice_state_update')
    async def music_voice(self,user,before,after):
        if after.channel == None and user.id == self.bot.user.id:
            try:
                self.player[user.guild.id]['queue'].clear()
            except KeyError:
                print(f"Failed to get guild id {user.guild.id}")



    async def filename_generator(self):
        chars=list(string.ascii_letters+string.digits)
        name=''
        for i in range(random.randint(9,25)):
            name+=random.choice(chars)
        
        if name not in self.player['audio_files']:
            return name

        
        return await self.filename_generator()


    async def playlist(self,data,msg):
        for i in data['queue']:
            self.player[msg.guild.id]['queue'].append({'title':i,'author':msg})



    async def queue(self,msg,song):
        title1=await Downloader.get_info(self,url=song)
        title=title1[0]
        data=title1[1]
        #NOTE:needs fix here
        if data['queue']:
            await self.playlist(data,msg)
            return await msg.send(f"Added playlist {data['title']} to queue") #NOTE: needs to be embeded to make it better output
        self.player[msg.guild.id]['queue'].append({'title':title,'author':msg})
        return await msg.send(f"**{title} added to queue**".title(),delete_after=60)



    async def voice_check(self,msg):
        """
        function used to make bot leave voice channel if music not being played for longer than 2 minutes
        """
        if msg.voice_client != None:
            await asyncio.sleep(120)
            if msg.voice_client != None and msg.voice_client.is_playing() == False and msg.voice_client.is_paused() == False:
                await msg.voice_client.disconnect()


    async def clear_data(self,msg):
        name=self.player[msg.guild.id]['name']
        os.remove(name)
        self.player['audio_files'].remove(name)


    async def loop_song(self,msg):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.player[msg.guild.id]['name']))
        loop=asyncio.get_event_loop()
        try:
            msg.voice_client.play(source, after=lambda a: loop.create_task(self.done(msg)))
            return 
        except AttributeError:
            #Has no attribute play
            pass


    async def done(self,msg):
        if msg.guild.id in self.player and self.player[msg.guild.id]['repeat'] is True:
            return await self.loop_song(msg)

        await self.clear_data(msg)

        if self.player[msg.guild.id]['queue']:
            queue_data=self.player[msg.guild.id]['queue'].pop(0)
            return await self.start_song(msg=queue_data['author'],song=queue_data['title'])


        else:
            self.player[msg.guild.id]['play']=False
            await self.voice_check(msg)
    

    async def start_song(self,msg,song):
        new_opts=ytdl_format_options.copy()
        audio_name=await self.filename_generator()

        self.player['audio_files'].append(audio_name)
        new_opts['outtmpl']=new_opts['outtmpl'].format(audio_name)

        ytdl=youtube_dl.YoutubeDL(new_opts)
        download1=await Downloader.video_url(song,ytdl=ytdl,loop=self.bot.loop)
        download1=await Downloader.video_url(song,ytdl=ytdl,loop=self.bot.loop)

        download=download1[0]
        data=download1[1]
        self.player[msg.guild.id]['name']=audio_name
        emb=discord.Embed(colour=0x419400, title='Now Playing',description=download.title,url=download.url)
        emb.set_thumbnail(url=download.thumbnail)
        emb.set_footer(text=f'Requested by {msg.author.name}',icon_url=msg.author.avatar_url)
        loop=asyncio.get_event_loop()
        msg.voice_client.play(download,after=lambda a: loop.create_task(self.done(msg)))

        if str(msg.guild.id) in self.music['guilds']: #adds user's default volume if in database
            msg.voice_client.source.volume=self.music['guilds'][str(msg.guild.id)]['vol']/100


        if data['queue']:
            await self.playlist(data,msg)

        await msg.send(embed=emb,delete_after=download.duration)
        self.player[msg.guild.id]['player']=download
        self.player[msg.guild.id]['author']=msg
        return msg.voice_client



    @command()
    async def play(self,msg,*,song):
        if msg.guild.id in self.player:
            if self.player[msg.guild.id]['play'] is True:
                return await self.queue(msg,song)

            if self.player[msg.guild.id]['queue']:
                return await self.queue(msg,song)

            if self.player[msg.guild.id]['play'] is False and not self.player[msg.guild.id]['queue']:
                return await self.start_song(msg,song)


        else:
            self.player[msg.guild.id]={
                'player':None,
                'queue':[],
                'play':True,
                'author':msg,
                'name':None,
                'repeat':False
            }
            return await self.start_song(msg,song)


    @play.before_invoke
    async def before_play(self,msg):
        """
        Check voice_client
            - User voice = None:
                please join a voice channel
            - bot voice == None:
                joins the user's voice channel
            - user and bot voice NOT SAME:
                - music NOT Playing AND queue EMPTY
                    join user's voice channel
                - items in queue:
                    please join the same voice channel as the bot to add song to queue
        """
    
        if msg.author.voice == None:
            return await msg.send('**Please join a voice channel to play music**'.title())

        if msg.voice_client == None: 
            return await msg.author.voice.channel.connect()


        if msg.voice_client.channel != msg.author.voice.channel:
            if msg.voice_client.is_playing() is False and not self.player[msg.guild.id]['queue']: #NOTE: Check player and queue 
                return await msg.voice_client.move_to(msg.author.voice.channel)
                #NOTE: move bot to user's voice channel if queue does not exist
            
            if self.player[msg.guild.id]['queue']:
                #NOTE: user must join same voice channel if queue exist
                return await msg.send("Please join the same voice channel as the bot to add song to queue")
            
        
    @command()
    async def repeat(self,msg):
        """
        Repeat the currently playing or turn off by using the command again
        `Ex:` .repeat
        """
        if msg.guild.id in self.player:
            if self.player[msg.guild.id]['play'] is True:
                if self.player[msg.guild.id]['repeat'] is True:
                    self.player[msg.guild.id]['repeat']=False
                    return await msg.message.add_reaction(emoji='✅')
                    
                self.player[msg.guild.id]['repeat']=True
                return await msg.message.add_reaction(emoji='✅')

            return await msg.send("No audio currently playing")
        return await msg.send("Bot not in voice channel or playing music")



    @command()
    async def skip(self,msg):
        if msg.author.voice != None:
            if msg.author.voice.channel != msg.voice_client.channel:
                return await msg.send("Please join the same voice channel as the bot")

        if msg.author.voice == None:
            return await msg.send("Please join the same voice channel as the bot")

        if msg.voice_client == None:
            return await msg.send("**No music currently playing**".title(),delete_after=60)
        
        else:
            if not self.player[msg.guild.id]['queue'] and self.player[msg.guild.id]['play'] is False:
                return await msg.send("**No songs in queue to skip**".title(),delete_after=60)

        
        await msg.send("**Skipping song...**".title(),delete_after=20)

        return msg.voice_client.stop()
    


    @commands.has_permissions(manage_channels=True)
    @command()
    async def stop(self,msg):
        if msg.author.voice != None and msg.voice_client != None:
            if  msg.voice_client.is_playing() == True or self.player[msg.guild.id]['queue']:
                self.player[msg.guild.id]['queue'].clear()
                msg.voice_client.stop()
                return await msg.voice_client.disconnect(), await msg.message.add_reaction(emoji='✅')



    @command(name='queue',aliases=['song-list','q','current-songs'])
    async def _queue(self,msg):
        if msg.voice_client != None:
            if msg.guild.id in self.player:
                if self.player[msg.guild.id]['queue']:
                    emb=discord.Embed(colour=0x419400, title='queue')
                    emb.set_footer(text=f'Command used by {msg.author.name}',icon_url=msg.author.avatar_url)
                    for i in self.player[msg.guild.id]['queue']:
                        emb.add_field(name=f"**{i['author'].author.name}**",value=i['title'],inline=False)
                    return await msg.send(embed=emb,delete_after=120)

        return await msg.send("No songs in queue")



    @command(name='current-song',aliases=['song?',''])
    async def nowplaying(self,msg):
        if msg.voice_client != None and msg.voice_client.is_playing() == True:
            emb=discord.Embed(colour=0x419400, title='Currently Playing',description=self.player[msg.guild.id]['player'].title)
            emb.set_footer(text=f"{self.player[msg.guild.id]['author'].author.name}",icon_url=msg.author.avatar_url)
            emb.set_thumbnail(url=self.player[msg.guild.id]['player'].thumbnail)
            return await msg.send(embed=emb,delete_after=120)
        
        return await msg.send(f"**No songs currently playing**".title(),delete_after=30)



    @command(aliases=['move-bot','move-b','mb','mbot'])
    async def join(self, msg, *, channel: discord.VoiceChannel=None):
        """
        Make bot join a voice channel you are in if no channel is mentioned
        `Ex:` .join
        `Ex:` .join Gen Voice
        """
        if msg.voice_client is not None:
            return await msg.send(f"Bot is already in a voice channel\nDid you mean to use {msg.prefix}moveTo")

        if msg.voice_client is None:
            if channel is None:
                return await msg.author.voice.channel.connect(), await msg.message.add_reaction(emoji='✅')
            
            return await channel.connect(), await msg.message.add_reaction(emoji='✅')
        
        else:
            if self.player[msg.guild.id]['play'] is False and not self.player[msg.guild.id]['queue']:
                return await msg.author.voice.channel.connect(), await msg.message.add_reaction(emoji='✅')


    @join.before_invoke
    async def before_join(self,msg):
        if msg.author.voice == None:
            return await msg.send("You are not in a voice channel")



    @join.error
    async def join_error(self,msg,error):
        if isinstance(error,commands.BadArgument):
            return msg.send(error)

        # if error.args[0] == 'Command raised an exception: Exception: queue':
        #     return await msg.send("**Please join the same voice channel as the bot to add song to queue**".title())

        if error.args[0] == 'Command raised an exception: Exception: playing':
            return await msg.send("**Please join the same voice channel as the bot to add song to queue**".title())



    @commands.has_permissions(manage_channels=True)
    @command(aliases=['vol'])
    async def volume(self,msg,vol:int):
        """
        Change the volume of the bot
        `Ex:` .vol 100
        `Ex:` .vol 150
        `Note:` 200 is the max
        `Permission:` manage_channels
        """
        
        if vol > 200:
            vol = 200
        vol=vol/100
        if msg.author.voice != None:
            if msg.voice_client != None:
                if msg.voice_client.channel == msg.author.voice.channel and msg.voice_client.is_playing() == True:
                    msg.voice_client.source.volume=vol
                    return await msg.message.add_reaction(emoji='✅')
                    


        
        return await msg.send("**Please join the same voice channel as the bot to use the command**".title(),delete_after=30)
    
    @volume.error
    async def volume_error(self,msg,error):
        if isinstance(error,commands.MissingPermissions):
            return await msg.send("Manage channels or admin perms required to change volume",delete_after=30)




def setup(bot):
    bot.add_cog(MusicPlayer(bot))