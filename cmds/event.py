import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension
from model.func import *
import sys
import logging
logger = logging.getLogger(__name__)


class event(Cog_Extension):

    _name = 'event'

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
        attachments = msg.attachments
        # print('ch_id:', channel_id, 'msg_id:', msg_id, 'aut_id:', author_id, 'con:', content, 'attach:', attachments)
        if attachments and msg.author != self.bot.user:
            file = attachments[0]
            file.filename = f"test_{file.filename}"
            spoiler = await file.to_file()
            await msg.channel.send(file=spoiler)
        """ if(msg.content == "check_channel_id"):
            print(f'Dc_msg: {msg.channel.id}')
        if msg.content == '<:MeMe:616147400792342538>' and msg.author != self.bot.user:
            await msg.channel.send('<:MeMe:616147400792342538>') """

    @commands.command()
    async def cleartest(self, ctx, number):
        channel_id = ctx.channel.id
        # print(channel_id)
        # channel = self.bot.get_channel(only_meme_speak_channel)
        # if channel_id == only_meme_speak_channel:
        mgs = []
        number = int(number)
        async for message in ctx.channel.history(limit=int(number)):
            mgs.append(message)
        for m in mgs:
            print(m.content)
        # await channel.delete_messages(mgs)

    @commands.command()
    async def event_test(self, ctx):
        async with ctx.typing():
            # do expensive stuff here
            await ctx.send('done!')

    @commands.command()
    async def event_test2(self, ctx):
        await ctx.send('test!')

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
    @commands.command()
    async def gc(self, ctx):
        print(ctx.channel.id)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload.message_id)


def setup(bot):
    bot.add_cog(event(bot))
