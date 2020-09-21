import discord
from discord.ext import commands
from core.classes import Cog_Extension
from model.func import *
import array


class Main(Cog_Extension):

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
    bot.add_cog(Main(bot))
