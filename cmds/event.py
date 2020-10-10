import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension
from model.func import *
import sys


class Event(Cog_Extension):

    """ @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(meme_channel)
        await channel.send(f'{member} join')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(meme_channel)
        await channel.send(f'{member} leave') """

    @commands.Cog.listener()
    async def on_message(self, msg):
        channel_id = msg.channel.id
        author_id = msg.author.id
        content = msg.content
        msg_id = msg.id
        # print('ch_id:',channel_id,'msg_id:',msg_id,'aut_id:',author_id,'con:',content)
        """ if(msg.content == "check_channel_id"):
            print(f'Dc_msg: {msg.channel.id}')
        if msg.content == '<:MeMe:616147400792342538>' and msg.author != self.bot.user:
            await msg.channel.send('<:MeMe:616147400792342538>') """

    @commands.command()
    async def cleartest(self, ctx, number):
        channel_id = ctx.channel.id
        # print(channel_id)
        channel = self.bot.get_channel(only_meme_speak_channel)
        if channel_id == only_meme_speak_channel:
            mgs = []
            number = int(number)
            n = 1
            async for message in ctx.channel.history():
                mgs.append(message)
                n = n + 1
                if(n > number):
                    break
            await channel.delete_messages(mgs)

    @commands.command()
    async def event_test(self, ctx):
        return 0

    @commands.command()
    async def get_msg_id(self, ctx, number):
        channel_id = ctx.channel.id
        channel = self.bot.get_channel(only_meme_speak_channel)
        if channel_id == only_meme_speak_channel:
            mgs = []
            number = int(number)
            n = 1
            async for message in ctx.channel.history():
                print(message.created_at, message.id)
                n += 1
                if n > number:
                    break


def setup(bot):
    bot.add_cog(Event(bot))
