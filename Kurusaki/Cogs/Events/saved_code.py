
#NOTE:LEAVING THIS SECTION FOR LATER USE WHEN PERMISSIONS ARE BETTER MANAGED
# if emote.custom_emoji is True and emote.emoji.id == 720232144538042368 and emote.message.guild is not None and user.guild_permissions.manage_messages is True and emote.message.author.id == self.bot.user.id: #IN GUILD
#     return await emote.message.delete()
# if emote.message.guild is None and emote.message.author.id == self.bot.user.id: #NOTE: INSIDE DM
#     return await emote.message.delete()

# if emote.message.author.id == user.id: #NOTE: SENDER IS AUTHOR
#     return await emote.message.delete()




#NOTE: SAVED FOR LATER WHEN PERMISSIONS BETTER MANAGED 
# @commands.is_owner()
# @command(hidden=True)
# async def logout(self,msg):
#     await self.bot.logout()
