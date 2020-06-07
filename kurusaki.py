import discord,asyncio
from discord.ext import commands



def get_prefix(bot, msg):

    prefixes = ['s.', 'a.','!']


    return commands.when_mentioned_or(*prefixes)(bot, msg)

bot = commands.Bot(command_prefix=get_prefix,description='Discord multiple command prefix')

@bot.event
async def on_ready():
    print(bot.user.name)



@bot.command()
async def test(msg,*,pack):
    perm_type=discord.Embed(title='Permissions Type')
    perm_type.add_field(name='General Permissions',value='❌')
    perm_type.add_field(name='All Permissions',value='✅')
    
    emb=discord.Embed(title="Role permission")
    emb.add_field(name='Create Instant Invites',value='1️⃣')
    emb.add_field(name='Kick Members',value='2️⃣')
    emb.add_field(name='Ban Members',value='3️⃣')
    emb.add_field(name='Administrator',value='4️⃣')
    emb.add_field(name='Manage Guild',value='5️⃣')
    emb.add_field(name='Add Reactions',value='6️⃣')
    emb.add_field(name='View Channel',value='7️⃣')
    emb.add_field(name='Send Messages',value='8️⃣')
    emb.add_field(name='Manage Messages',value='9️⃣')
    emb.add_field(name='Attack Files',value='9️⃣')
    emb.add_field(name='Read Message History',value='9️⃣')
    emb.add_field(name='Mention Everyone',value='9️⃣')
    emb.add_field(name='External Emojis',value='9️⃣')
    emb.add_field(name='Mute Members',value='9️⃣')
    emb.add_field(name='Deafen Members',value='9️⃣')
    emb.add_field(name='Move Members',value='9️⃣')
    emb.add_field(name='Change Nickname',value='9️⃣')
    emb.add_field(name='Manage Nicknames',value='9️⃣')


bot.run('NDA1OTA3MzI2MDUxMDI0OTA2.XjJdZA.7EBDDEZ-SIX0FofndFy2Kfv9rBs')
