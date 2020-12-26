import discord, os
from discord.ext import commands
from discord.ext.commands import command, Cog
import random, time, typing,asyncio



async def random_color():
    color = discord.Color.from_rgb(random.randint(0,256),random.randint(0,256),random.randint(0,256))
    return color


async def edit_reason(user,reason=None):
    if reason is None:
        return f"{user.name}({user.id})"

    return f"{reason}: {user.name}({user.id})"



async def list_breaker(List,amt):
    new=[]
    div = len(List)//amt
    piece = len(List) - div * amt 
    cmin = 0 
    cmax= div
    for i in range(amt):
        if i == amt-1:
            new.append(List[cmin:])
        else:
            new.append(List[cmin:cmax])
        cmin = cmax
        cmax += div

    return new


