import discord
from discord.ext import commands
from core.classes import Cog_Extension
from model.func import *
import array
import os
import logging
logger = logging.getLogger(__name__)


class main(Cog_Extension):

    _name = 'main'
    # main_str = """\n{
    #     channel_id:,
    #     msg_id:,\n}"""
    # main_data = {}

    # def __init__(self, bot):
    #     print('init')
    #     print(__file__)
    #     super().__init__(bot)
    #     with open('./data/mangage.json', 'r', encoding='utf8') as jfile:
    #         self.main_data = json.load(jfile)
    #     print('get main data')

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     if os.path.isfile('./mangage.json'):
    #         with open('./data/mangage.json', 'r', encoding='utf8') as jfile:
    #             self.main_data = json.load(jfile)

    # @commands.command()
    # async def _check(self, ctx):
    #     try:
    #         channel_id = self.main_data['channel_id']
    #         msg_id = self.main_data['msg_id']
    #         channel = self.bot.get_channel(channel_id)
    #         if not channel:
    #             print('channel not find')
    #             return False
    #         msg = await channel.fetch_message(msg_id)
    #         if not msg:
    #             print('msg not find')
    #             return False
    #         content = msg.content
    #         await ctx.send('main has get')
    #     except:
    #         #if not self.main_data:
    #         channel_id = ctx.channel.id
    #         msg = await ctx.send(self.main_str)
    #         msg_id = msg.id
    #         self.main_data['channel_id'] = channel_id
    #         self.main_data['msg_id'] = msg_id
    #         self.main_save()

    # @commands.command()
    # async def _change(self, ctx, msg):
    #     pass

    # @commands.command()
    # async def main_test(self, ctx):
    #     channel = self.bot.get_channel(self.main_data['channel_id'])
    #     if not channel:
    #         print('channel not find')
    #         return False
    #     msg = await channel.fetch_message(self.main_data['msg_id'])
    #     if not msg:
    #         print('msg not find')
    #         return False

    # def main_save(self):
    #     f = open("./data/main.json", "w")
    #     f.write(json.dumps(self.main_data))
    #     f.close()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    @commands.command()
    async def say(self, ctx, *, msg):
        author_id = ctx.author.id
        if(admin_check(author_id, self.bot) == True):
            """ print(msg) """
            await ctx.message.delete()
            await ctx.send(msg.format(ctx=ctx))

    @commands.command()
    async def leave(self, ctx):
        author_id = ctx.author.id
        if(admin_check(author_id, self.bot) == True):
            await self.bot.close()

    @commands.command()
    async def login(self, ctx):
        author_id = ctx.author.id
        if(admin_check(author_id, self.bot) == True):
            await self.bot.login()

    @commands.command()
    async def logout(self, ctx):
        author_id = ctx.author.id
        if(admin_check(author_id, self.bot) == True):
            await self.bot.logout()

    """  @commands.command()
    async def add_admin(self, ctx, msg):
        author_id = ctx.author.id
        if(admin_check(author_id,self.bot) == True):
            tmp = msg.replace("<", "")
            tmp = tmp.replace("@", "")
            tmp = tmp.replace("!", "")
            tmp = tmp.replace(">", "")
            setting_data["admin"].insert(len(setting_data["admin"]), int(tmp))
            await ctx.send(f'{msg}已加入ミミ管理員')
            admin_save()

    @commands.command()
    async def del_admin(self, ctx, msg):
        author_id = ctx.author.id
        if(admin_check(author_id,self.bot) == True):
            tmp = msg.replace("<", "")
            tmp = tmp.replace("@", "")
            tmp = tmp.replace("!", "")
            tmp = tmp.replace(">", "")
            for k in setting_data["admin"]:
                if(int(tmp) == k):
                    setting_data["admin"].remove(int(tmp))
                    await ctx.send(f'{msg}已退出ミミ管理員')
                    admin_save()
    """
    @commands.command()
    async def show_admin(self, ctx):
        tmp_str = ""
        members = get_role_members(self.bot)
        for k in members:
            tmp_str = tmp_str + f'<@!{k}> \n'
        await ctx.send(f'{tmp_str}是ミミ管理員')

    """ @commands.command()
    async def admin_test(self, ctx):
        self.get_role_members() """


def setup(bot):
    bot.add_cog(main(bot))
