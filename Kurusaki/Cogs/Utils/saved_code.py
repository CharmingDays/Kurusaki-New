
#NOTE:LEAVING THIS SECTION FOR LATER USE WHEN PERMISSIONS ARE BETTER MANAGED
# if emote.custom_emoji is True and emote.emoji.id == 720232144538042368 and emote.message.guild is not None and user.guild_permissions.manage_messages is True and emote.message.author.id == self.bot.user.id: #IN GUILD
#     return await emote.message.delete()
# if emote.message.guild is None and emote.message.author.id == self.bot.user.id: #NOTE: INSIDE DM
#     return await emote.message.delete()

# if emote.message.author.id == user.id: #NOTE: SENDER IS AUTHOR
#     return await emote.message.delete()







    # @commands.Cog.listener('on_command_error')
    # async def all_command_error(self,msg,error):
    #     #TODO: Attempt to make a correction suggestion here using `re` lib
    #     if isinstance(error,commands.CommandOnCooldown):
    #         return await msg.send(f"Command is on cooldown, please try again in {round(error.cooldown.retry_after,2)} seconds")

    
    #     if isinstance(error,commands.CommandError):
    #         if '60003' in error.args[0]:
    #             return await msg.send("Two factor is enabled for the server, please disable it temporarily to use the command")

    #         else:
    #             return error

    #     if isinstance(error,commands.PrivateMessageOnly):
    #         return await msg.send("This command can only be used inside a private message (PM/DM)")

    #     if error is commands.NoPrivateMessage:
    #         return await msg.send("Command unable to run inside a private message (PM/DM")


    #     if isinstance(error,commands.CommandNotFound) and msg.guild is not None and msg.guild.id != 264445053596991498:
    #         content=msg.message.content.replace(f"{msg.prefix}","")
    #         return await msg.send(f"Command {content} is not found")


    #     if isinstance(error,commands.NotOwner):
    #         return await msg.send("This command is only for the bot owners")

    #     print(error)








#NOTE: SAVED FOR LATER WHEN PERMISSIONS BETTER MANAGED 
# @commands.is_owner()
# @command(hidden=True)
# async def logout(self,msg):
#     await self.bot.logout()


    async def chat_bot(self,query):
        """
        Request query to the api.ai for chat bot
        """
        TOKEN="ad1c55f60a78435195cd95fc4bba02e9"
        BASE_URL=f"https://api.dialogflow.com/v1/query?v=20150910&sessionId=12345&lang=en&query={query}"
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        r=rq.get(url=BASE_URL,headers=headers)
        return r


#NOTE: saved for Michelle's AI chat coding 
# @commands.Cog.listener('on_message')
# async def message_tracker(self,msg):
#     if not isinstance(msg.channel,discord.TextChannel):
#         return None

#     if msg.author.bot is True:
#         return None

#     if msg.guild.id in [251397504879296522,295717368129257472]:
#         if f"<@!{self.bot.user.id}>" in msg.content:
#             content=msg.content.replace(f'<@!{self.bot.user.id}> ','')
#             data=await self.chat_bot(content)
#             if data.ok:
#                 reply=data.json()['result']['fulfillment']['speech']
#                 if reply == '#love':
#                     not_yukinno=[f"Sorry {msg.author.name}, but I'm already taken by someone","I'm already taken \:)",f"Sorry, I'm already taken {msg.author.name}"]
#                     is_yukinno=['❤','<3','I ❤ you',f'I love you {msg.author.display_name}',f'My love is only for you {msg.author.name}']
#                     if msg.author.id == self.michelley:
#                         return await msg.channel.send(random.choice(is_yukinno))
#                     else:
#                         return await msg.channel.send(random.choice(not_yukinno))

#                 return await msg.channel.send(reply)
#             if not data.ok:
#                 return await msg.channel.send("Sorry, I'm experiencing some technical issues, please try again later D:")
                