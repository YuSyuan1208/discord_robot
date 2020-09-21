"""
font color

 ```css
test
```
 ```yaml
test
```
 ```http
test
```
 ```arm
test
```
"""

import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
import array
from model.func import *
import sys


""" img_url_list = team_fight_setting['img_url_list']
unit_list = team_fight_setting['unit_list']
embed_color_list = team_fight_setting['embed_color_list']
number_emoji = team_fight_setting['number_emoji']
sign_up_emoji = team_fight_setting['sign_up_emoji']
cancel_emoji = team_fight_setting['cancel_emoji']
overflow_emoji = team_fight_setting['overflow_emoji']
overflow_cancel_emoji = team_fight_setting['overflow_cancel_emoji'] """
img_url_list = {"1王": "https://cdn.discordapp.com/attachments/680402200077271106/702486233976274954/a20f65fafc6ab134dee66e9e03b2e07e.png",
                "2王": "https://cdn.discordapp.com/attachments/680402200077271106/702486290012307517/75edbc7700db07e068ffbbe1e14fdf71.png",
                "3王": "https://cdn.discordapp.com/attachments/680402200077271106/702486362065993728/ee8ccd72f075340d5105c38903681e7b.png",
                "4王": "https://cdn.discordapp.com/attachments/680402200077271106/702486425844580362/gateway-3-1.png",
                "5王": "https://cdn.discordapp.com/attachments/680402200077271106/702486472317730816/gateway-4-1.png",
                "補償清單": "https://cdn.discordapp.com/attachments/680402200077271106/681015805110124554/616147400792342538.png",
                "出刀清單": "https://cdn.discordapp.com/attachments/680402200077271106/681015805110124554/616147400792342538.png"}
unit_list = {"1王": "W",
             "2王": "W",
             "3王": "W",
             "4王": "W",
             "5王": "W",
             "補償清單": "S",
             "出刀清單": "W"}
embed_color_list = {"可報_無補": 0xaae3aa,
                    "可報_有補": 0xffdc5e,
                    "不可報": 0xe38fa5,
                    "補償清單": 0xffffff,
                    "出刀清單": 0xffffff, }


number_emoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣',
                '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '⬅️', '▶️']

sign_up_emoji = '📄'
cancel_emoji = '🔄'
overflow_emoji = '🔂'
overflow_cancel_emoji = '🆖'

# *刪除列表 / *Clear


class Team_Fight(Cog_Extension):
    """ ----------------- 戰隊戰 help -----------------"""
    @commands.command()
    async def 戰隊戰(self, ctx):
        # TODO: 戰隊戰指令說明
        embed = discord.Embed(
            title="戰隊戰專用指令", description="英文指令不區分大小寫", color=0x99d8ff)
        embed.add_field(
            name="查看排隊狀況", value="*清單 / *List / *L / *List 1 ", inline=False)
        embed.add_field(name="查看單隻王排隊狀況 （Ex: 搜尋 1 1 5）<指令 王 周目 周目>",
                        value="*搜尋 / *Search / *s", inline=False)
        embed.add_field(name="報名/喊刀（Ex: 報名 1 300 1）<指令 王 傷害 周目>",
                        value="*報名 / *Enter / *e", inline=False)
        embed.add_field(name="更改預估傷害 （Ex: 更改 1 1 400 1）<指令 王 排序 傷害 周目>",
                        value="*更改 / *change / *c", inline=True)
        embed.add_field(name="取消報名出刀 （Ex: 取消 1 1 1 ）<指令 王 排序 周目 >",
                        value="*取消 / *取消報名 / *recall / *r", inline=False)
        embed.add_field(name="補償排程 （Ex: 補償 1 30 2）<指令 王 秒數 周目>",
                        value="*補償 / *Overflow / *o", inline=True)
        # embed.add_field(name="切換周目（Ex: 切換周 1）<指令 周目>", value="切換周", inline=False)
        embed.add_field(name="尾刀員指令 （Ex:）",
                        value="*收 / *Finish / *f", inline=False)
        embed.add_field(name="顯示 目前周 目前王", value="*當周 *當王", inline=True)
        embed.add_field(name="*", value="未輸入 周目 皆為 當周", inline=False)
        embed.set_footer(text="管理員可取消其他人的報名及刪除列表")
        await ctx.send(embed=embed)
    """ ----------------- 戰隊戰 help -----------------"""

    """ ----------------- 報名相關指令 -----------------"""
    @commands.command(name='報名',
                      description="Ex. *報名 ?王 100(預估傷害)\nEx. *報名 補償清單(6) 100(剩餘秒數) ?王",
                      brief="Ex. *報名 ?王 100(預估傷害)\nEx. *報名 補償清單(6) 100(剩餘秒數) ?王",
                      aliases=['enter', 'e'])
    async def 報名(self, ctx, *msg):
        # TODO: 報名指令
        force_week = now['force_week']
        if(str(type(ctx)) == "<class 'discord.channel.TextChannel'>"):
            channel_id = ctx.id
            author_id = msg[3]
            delete_after = 5
            delete_msg = '(5秒後清除)'
        else:
            channel_id = ctx.channel.id
            author_id = ctx.author.id
            delete_after = None
            delete_msg = ''
        ''' 權限 '''
        if (admin_check(author_id, self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel, only_meme_speak_channel, run_out_before_look]):
                    return 0

        ''' 周、王判定 '''
        # try:
        king = tea_fig_KingIndexToKey(All_OutKnife_Data[1], msg[0])
        if(king in ["補償清單", "出刀清單"]):
            week = now['周']
        else:
            try:
                week = int(msg[2])
            except:
                week = now['周']
        # print("test")
        if(week > now['limit_max_week']):
            li_temp = now['limit_max_week']
            send_msg = f'<@!{author_id}>報名:{force_week}周 限制:{li_temp}周，報名失敗{delete_msg}'
            await ctx.send(send_msg, delete_after=delete_after)
            if(run_out_before_look):
                channel2 = self.bot.get_channel(run_out_before_look)
                await channel2.send(send_msg)
            return 0
        tmp = {}
        tmp[0] = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg[0])
        tmp[1] = msg[1] if len(msg) > 1 else ''

        ''' meme deit index '''
        try:
            if(tmp[0] == "補償清單"):
                meme_king = 6
            elif(tmp[0] == "出刀清單"):
                meme_king = 7
            else:
                meme_king = int(tmp[0][0])
            meme_index = (week - now['周']) * list_refresh_king + meme_king - 1
            meme_in_index = (week - now['周']) * list_refresh_king + now['王'] - 1
        except:
            print("meme_edit para fail")

        ''' 清單資訊獲取 '''
        # tmp = f'{msg[0]}'.split(',')
        SignUp_List = All_OutKnife_Data[week][tmp[0]]["報名列表"]
        damage_in = int(tmp[1]) if tmp[1] != '' else 0
        king_hp = All_OutKnife_Data[week][tmp[0]]["資訊"]["hp"]

        ''' 報名參數規則判定 '''
        dc_re = [True, ""]
        # print(tmp[0])
        if(tmp[0] == "補償清單"):
            tmp[2] = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg[2])
            try:
                asd = All_OutKnife_Data[week][tmp[2]]
            except:
                await ctx.send(f'<@!{author_id}>王輸入錯誤 {delete_msg}', delete_after=delete_after)
                return 0
            damage_in = f'{tmp[2]} {damage_in}'
        elif(tmp[0] == "出刀清單"):
            pass
        elif(tmp[0] != "補償清單"):
            dc_re = tea_fig_DamageCheck(
                SignUp_List, damage_in, king_hp, author_id)
        if(dc_re[0] == False):
            await ctx.send(f'{dc_re[1]}{delete_msg}', delete_after=delete_after)
            return 0

        ''' 報名資料存入 '''
        if (tmp[0] in All_OutKnife_Data[week].keys()):
            if (len(tea_fig_list_check(SignUp_List, f'<@!{author_id}>')) < list_max_enter):
                l = len(SignUp_List)
                SignUp_List.insert(
                    l, {"id": f'<@!{author_id}>', "傷害": damage_in, "呼叫": 0, "進場": 0})
                if(tmp[0] == "補償清單"):

                    await ctx.send(f'<@!{author_id}>{tmp[0]}報名成功٩( >ω< )وو, 目前人數: {l+1} {delete_msg}', delete_after=delete_after)
                    """ if(week <= now['周'] + 2):
                        # print('meme_edit')
                        await self.meme_edit(ctx, week, meme_king, meme_index) """
                elif(tmp[0] == "出刀清單"):
                    tea_fig_cut_out_list_sort()
                    await ctx.send(f'{tmp[0]}進場成功٩( >ω< )وو, 目前人數: {l+1} {delete_msg}', delete_after=delete_after)
                    In_SignUp_List = All_OutKnife_Data[week][str(now['王'])+'王']["報名列表"]
                    in_index = tea_fig_list_check(In_SignUp_List, f'<@!{author_id}>')
                    In_SignUp_List[in_index[0]]['進場'] += 1
                    await self.meme_edit(ctx, week, now['王'], meme_in_index)
                else:
                    send_msg = f'<@!{author_id}>{force_week}周{tmp[0]}報名成功٩( >ω< )وو, 目前人數: {l+1} {delete_msg}'
                    await ctx.send(send_msg, delete_after=delete_after)
                    if(run_out_before_look):
                        channel2 = self.bot.get_channel(run_out_before_look)
                        await channel2.send(send_msg)

                if(week <= now['周'] + 2):
                    # print('meme_edit')
                    await self.meme_edit(ctx, week, meme_king, meme_index)
            else:
                await ctx.send(f'<@!{author_id}>報名失敗, 已在列表中或超過上限(最多1筆){delete_msg}', delete_after=delete_after)
        await self.data輸出(ctx)
        """ except:
            await ctx.send(tea_fig_error_message())#f'<@!{author_id}>報名失敗，請確認有沒有錯字或超出範圍以及預估傷害(´•ω•｀)\nEx. *報名 ?王 100(預估傷害)\nEx. *報名 補償清單(6) 100(剩餘秒數) ?王')
            print(sys.exc_info()) """

    @commands.command(name='取消報名',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['取消', 'r', 'recall'])
    async def 取消報名(self, ctx, *msg):
        force_week = now['force_week']
        if(str(type(ctx)) == "<class 'discord.channel.TextChannel'>"):
            channel_id = ctx.id
            author_id = msg[3]
            delete_after = 5
            delete_msg = '(5秒後清除)'
        else:
            channel_id = ctx.channel.id
            author_id = ctx.author.id
            delete_after = None
            delete_msg = ''

        ''' 權限 '''
        if (admin_check(author_id, self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel, only_meme_speak_channel, run_out_before_look]):
                    return 0
        try:
            week = int(msg[2])
        except:
            week = now['周']
        try:
            # tmp = f'{msg[0]}'.split(',')
            tmp = {}

            tmp[0] = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg[0])
            tmp[1] = msg[1]
            ''' meme edit'''
            try:
                if(tmp[0] == "補償清單"):
                    meme_king = 6
                elif(tmp[0] == "出刀清單"):
                    meme_king = 7
                else:
                    meme_king = int(tmp[0][0])
                meme_index = (week - now['周']) * list_refresh_king + meme_king - 1
            except:
                print("meme_edit para fail")

            SignUp_List = All_OutKnife_Data[week][tmp[0]]["報名列表"]
            # if(len(tmp) > 1):
            in_id = int(tmp[1])
            list_len = len(SignUp_List)
            # print(in_id)
            # print(list_len)
            if((admin_check(author_id, self.bot) == True) or (f'<@!{author_id}>' == All_OutKnife_Data[week][tmp[0]]["報名列表"][in_id-1]["id"])):
                # for v in data:
                #    if(v["id"] == f'{in_id}'):
                if(list_len >= in_id):
                    All_OutKnife_Data[week][tmp[0]]["報名列表"].pop(in_id-1)
                    await ctx.send(f'<@!{author_id}>取消報名{force_week}周{tmp[0]}大成功٩(ˊᗜˋ*)و{delete_msg}', delete_after=delete_after)
                    if(week <= now['周'] + 2):
                        # print('meme_edit')
                        await self.meme_edit(ctx, week, meme_king, meme_index)
                else:
                    # return 1
                    await ctx.send(f'<@!{author_id}>取消報名失敗，名單找不到你耶(๑•́︿•̀๑)({tmp[0]} No.{in_id}){delete_msg}', delete_after=delete_after)
            else:
                await ctx.send(f'<@!{author_id}>你沒有權限刪除別人喔(๑•́︿•̀๑){delete_msg}', delete_after=delete_after)
        except:
            # '欲取消報名請標註特定王(ฅฅ*)\nEx. \*取消報名 ?王 ?(No.)')
            await ctx.send(f'{tea_fig_error_message()}{delete_msg}', delete_after=delete_after)
            print(sys.exc_info())
        await self.data輸出(ctx)

    """ @commands.command(name='更改傷害',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['更改', 'change', 'c'])
    async def 更改傷害(self, ctx, *msg):
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if (admin_check(author_id,self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel]):
                    return 0
        try:
            week = int(msg[3])
        except:
            week = now['周']
        try:
            # tmp = f'{msg[0]}'.split(',')
            tmp = {}
            tmp[0] = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg[0])
            if(tmp[0] in ["補償清單","出刀清單"]):
                await ctx.send(f'<@!{author_id}>{tmp[0]}不開放修改喔(๑•́︿•̀๑) ')
                return 0
            tmp[1] = msg[1]
            tmp[2] = msg[2]
            ''' meme deit '''
            try:
                meme_king = int(tmp[0][0])
                meme_index = (week - now['周']) * list_refresh_king + meme_king - 1
            except:
                print("meme_edit para fail")
            in_id = int(tmp[1])
            damage_in = int(tmp[2])
            SignUp_List = All_OutKnife_Data[week][tmp[0]]["報名列表"]
            king_hp = All_OutKnife_Data[week][tmp[0]]["資訊"]["hp"]

            dc_re = [True, ""]
            if(tmp[0] not in ["補償清單","出刀清單"]):
                dc_re = tea_fig_DamageCheck(
                    SignUp_List, damage_in, king_hp, author_id,  in_id)
            if(dc_re[0] == False):
                await ctx.send(dc_re[1])
                return 0

            if(f'<@!{author_id}>' == All_OutKnife_Data[week][tmp[0]]["報名列表"][in_id-1]["id"]):
                All_OutKnife_Data[week][tmp[0]
                                        ]["報名列表"][in_id-1]["傷害"] = damage_in
                await ctx.send(f'<@!{author_id}>修改傷害成功')
                if(week <= now['周'] + 2):
                    # print('meme_edit')
                    await self.meme_edit(ctx, week, meme_king, meme_index)
            else:
                await ctx.send(f'<@!{author_id}>你沒有權限修改別人喔(๑•́︿•̀๑)')
        except:
            await ctx.send(f'<@!{author_id}>修改失敗 ')
            print(sys.exc_info()[0]) """

    """ @commands.command(name='補償',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['overflow', 'o'])
    async def 補償(self, ctx, *msg):
        force_week = now['force_week']
        if(str(type(ctx)) == "<class 'discord.channel.TextChannel'>"):
            channel_id = ctx.id
            author_id = msg[3]
            delete_after = 5
            delete_msg = '(5秒後清除)'
        else:
            channel_id = ctx.channel.id
            author_id = ctx.author.id
            delete_after = None
            delete_msg = ''
        if (admin_check(author_id,self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel, only_meme_speak_channel]):
                    return 0
        try:
            to_list = msg[2]
            to_list = to_list.lower()
        except:
            to_list = ""
            to_list = to_list.lower()
        if(to_list == "later"):
            try:
                week = int(msg[3])
            except:
                week = now['周']
        else:
            try:
                week = int(msg[2])
            except:
                week = now['周']
        if(week > now['limit_max_week']):
            li_temp = now['limit_max_week']
            send_msg = f'<@!{author_id}>報名:{force_week}周 限制:{li_temp}周，報名失敗{delete_msg}'
            await ctx.send(send_msg, delete_after=delete_after)
            if(run_out_before_look):
                channel2 = self.bot.get_channel(run_out_before_look)
                await channel2.send(send_msg)
            return 0
        try:
            tmp = {}
            tmp[0] = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg[0])
            tmp[1] = msg[1]
            ''' meme deit '''
            try:

                meme_king = int(tmp[0][0])
                meme_index = (week - now['周']) * list_refresh_king + meme_king - 1
            except:
                print("meme_edit para fail")

            if(to_list == "later"):
                await self.報名(ctx, '補償清單', tmp[1], tmp[0])
                return 0
            All_OutKnife_Data[week][tmp[0]
                                    ]["資訊"]["header"] = f'<@!{author_id}> {tmp[1]}S(補償)'

            send_msg = f'<@!{author_id}>{force_week}周{tmp[0]}補償刀登記成功{delete_msg}'
            await ctx.send(send_msg, delete_after=delete_after)
            if(run_out_before_look):
                channel2 = self.bot.get_channel(run_out_before_look)
                await channel2.send(send_msg)
            if(week <= now['周'] + 2):
                # print('meme_edit')
                await self.meme_edit(ctx, week, meme_king, meme_index)
        except:
            pass
        await self.data輸出(ctx)
        # await ctx.send('補償報名失敗，請確認有沒有錯誤格式(´•ω•｀)\nEx. *補償 ？王  30（補償秒數）/ *補償 ？王  30（補償秒數）+  later') """

    """ @commands.command(name='取消補償刀',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=[])
    async def 取消補償刀(self, ctx, *msg):
        force_week = now['force_week']
        if(str(type(ctx)) == "<class 'discord.channel.TextChannel'>"):
            channel_id = ctx.id
            author_id = msg[2]
            delete_after = 5
            delete_msg = '(5秒後清除)'
        else:
            channel_id = ctx.channel.id
            author_id = ctx.author.id
            delete_after = None
            delete_msg = ''
        ''' 權限 '''
        if(admin_check(author_id,self.bot) != True):
            if (limit_enable):
                if (channel_id not in [tea_fig_channel, only_meme_speak_channel]):
                    return 0

        try:
            week = int(msg[1])
        except:
            week = now['周']
        tmp = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg[0])
        header = All_OutKnife_Data[week][tmp]['資訊']['header']
        id = header.split('>')
        id = f'{id[0]}>'
        try:
            if((admin_check(author_id,self.bot) == True) or (f'<@!{author_id}>' == id)):
                sel_king = tea_fig_KingIndexToKey(
                    All_OutKnife_Data[week], msg[0])
                All_OutKnife_Data[week][sel_king]["資訊"]["header"] = ""
                await ctx.send(f'<@!{author_id}>{force_week}周{msg[0]}取消補償刀成功{delete_msg}', delete_after=delete_after)
                try:
                    if(sel_king == "補償清單"):
                        meme_king = 6
                    elif(sel_king == "出刀清單"):
                        meme_king = 7
                    else:
                        meme_king = int(msg[0].split('王')[0])
                    meme_index = (week - now['周']) * list_refresh_king + meme_king - 1
                except:
                    print("meme_edit para fail")
                if(week <= now['周'] + 2):
                    # print('meme_edit')
                    await self.meme_edit(ctx, week, meme_king, meme_index)

            else:
                await ctx.send(f'<@!{author_id}>你沒有權限刪除別人喔(๑•́︿•̀๑){delete_msg}', delete_after=delete_after)
        except:
            pass
        await self.data輸出(ctx) """

    @commands.command(name='清單',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['list', 'l'])
    async def 清單(self, ctx, *msg):
        force_week = now['force_week']
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if (admin_check(author_id, self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel]):
                    return 0
        """ try:
            week = int(msg[1])
        except: """
        week = now['周']
        try:
            if(len(msg) == 0):
                msg = "all"
            else:
                msg = msg[0]
            if msg == "all":
                await ctx.send(f'```{force_week}周```')
                for k in range(0, len(All_OutKnife_Data[week])):
                    tmp = tea_fig_list_func([k+1, week])
                    await ctx.send(embed=tmp[1])
            else:
                tmp = tea_fig_list_func([msg, week])
                await ctx.send(f'```{force_week}周```')
                await ctx.send(embed=tmp[1])
        except:
            await ctx.send("```arm\n欲查詢列表請標注特定王(ฅฅ*)\n``` ex. \*列表 all ,\*列表 ?王")
            print(sys.exc_info()[0])
    """ ----------------- 報名相關指令 -----------------"""

    """ ----------------- 補償相關指令 -----------------"""
    @commands.command(name='補償清單',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['ol'])
    async def 補償清單(self, ctx):
        SignUp_List = overflow['報名列表']
        for i in SignUp_List:
            await ctx.send(f'{i["id"]} {i["傷害"]}')

    """ ----------------- 補償相關指令 -----------------"""

    """ ----------------- 出刀相關指令 -----------------"""
    @commands.command(name='進刀',
                      aliases=['in'])
    async def 進刀(self, ctx):
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if(limit_enable):
            if (channel_id not in [run_out_before_look]):
                return 0
        week = now['周']
        king_index = now['王']
        force_week = now['force_week']
        king = tea_fig_KingIndexToKey(All_OutKnife_Data[1], king_index)
        SignUp_List = All_OutKnife_Data[week][king]['報名列表']
        index = tea_fig_list_check(SignUp_List, f'<@!{author_id}>')
        if len(index) > 0:
            await self.報名(ctx, 7)
        else:
            await ctx.send(f'尚未報名{force_week}周{king}清單')

    @commands.command(name='回報',
                      aliases=['re'])
    async def 回報(self, ctx, *msg):
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if(limit_enable):
            if (channel_id not in [run_out_before_look]):
                return 0
        week = now['周']
        king = 7
        try:
            damage = int(msg[0])
        except:
            await ctx.send(f'<@!{author_id}>傷害輸入錯誤')
            return False
        info = {'傷害': damage, '備註': ' '.join(msg[1:])}
        meme_index = (week - now['周']) * list_refresh_king + king - 1
        SignUp_List_tmp = All_OutKnife_Data[week]['出刀清單']["報名列表"]
        if tea_fig_enter_info_change(SignUp_List_tmp, author_id, info):
            await ctx.send(f'回報成功')
            await self.meme_edit(ctx, week, king, meme_index)
        else:
            await ctx.send(f'<@!{author_id}>尚未進刀，請輸入*in進場')

    @commands.command(name='掛樹', aliases=['tree'])
    async def 掛樹(self, ctx):
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if(limit_enable):
            if (channel_id not in [run_out_before_look]):
                return 0
        week = now['周']
        king = 7
        info = {'tree': 1}
        meme_index = (week - now['周']) * list_refresh_king + king - 1
        SignUp_List_tmp = All_OutKnife_Data[week]['出刀清單']["報名列表"]
        if tea_fig_enter_info_change(SignUp_List_tmp, author_id, info):
            await ctx.send(f'掛樹成功')
            await self.meme_edit(ctx, week, king, meme_index)
        else:
            await ctx.send(f'<@!{author_id}>尚未進刀，請輸入*in進場')

    @commands.command(name='掛樹清單', aliases=['tl'])
    async def 掛樹清單(self, ctx):
        author_id = ctx.author.id
        if (admin_check(author_id,self.bot) != True):
            return False
        SignUp_List = ReportDamage['報名列表']
        content = ''
        for i in SignUp_List:
            if 'tree' in i:
                content += f' {i["id"]}'
        if content:
            await ctx.send(f'{content}下來啦，是要在樹上多久!')
    """ ----------------- 出刀相關指令 -----------------"""

    """ ----------------- 週數 -----------------"""
    @commands.command()
    async def 當周(self, ctx):
        force_week = now['force_week']
        week = now['周']
        await ctx.send(f'```{force_week}周```')

    ''' @commands.command()
    async def 下周(self, ctx):
        channel_id = ctx.channel.id
        author_id = ctx.author.id

        if (admin_check(author_id,self.bot) != True):
            if (limit_enable):
                if (channel_id not in [tea_fig_channel]):
                    return 0
        week = now['周']
        week += 1
        now['周'] = week
        await self.now輸出(ctx)
        # await ctx.send(f'```{week}周```') '''

    @commands.command()
    async def 切換周(self, ctx, msg):
        # 只切換force_week
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if (admin_check(author_id, self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel]):
                    return 0
        week = now['force_week']
        week = int(msg)
        now['force_week'] = week
        await ctx.send(f'切換周成功')
        await self.now輸出(ctx)
        await self.now_edit(ctx)
        await self.meme_edit(ctx, 'all')

    """ @commands.command(name='看王',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['search', 's'],
                      )
    async def 看王(self, ctx, *msg):
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if (admin_check(author_id,self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel]):
                    return 0
        week = now['周']
        tmp = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg[0])
        start_week = int(msg[1])
        end_week = int(msg[2]) + 1
        if(abs(start_week - end_week) <= 5):
            for i in range(start_week, end_week):
                # await self.切換周(ctx,i)
                await self.清單(ctx, tmp, i)
            # await self.切換周(ctx,week)
            return 0
        await ctx.send('區間請小於5') """
    """ ----------------- 週數 -----------------"""

    """ ----------------- 王數 -----------------"""
    @commands.command()
    async def 當王(self, ctx):
        king = now['王']
        await ctx.send(f'```{king}王```')

    @commands.command(name='下王',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['finsh', 'f', '收'],
                      )
    async def 下王(self, ctx, *msg):
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if(limit_enable):
            if (channel_id not in [run_out_before_look]):
                return 0
        if (admin_check(author_id, self.bot) == True):
            if(len(msg) > 0):
                symbol_array = ['!', '@', '<', '>']
                tmp_id = msg[0]
                for i in symbol_array:
                    tmp_id = tmp_id.replace(i, '')
                author_id = int(tmp_id)
        send_msg = ''
        king = now['王']
        week = now['周']

        # 清單人員比對
        user_index = 0
        damage = 0
        # try:
        msg_index = [
            msg_index for msg_index in list_msg_tmp if list_msg_tmp_id[king-1] in [msg_index[2].id]][0]
        week_data = msg_index[0]
        king_data = tea_fig_KingIndexToKey(
            All_OutKnife_Data[1], msg_index[1])

        if len(tea_fig_list_check(All_OutKnife_Data[week_data][king_data]['報名列表'], f'<@!{author_id}>')) > 0:
            used_list = [tmp['id']
                         for tmp in All_OutKnife_Data[week_data][king_data]['報名列表']]
            user_index = used_list.index(f'<@!{author_id}>')
            damage = All_OutKnife_Data[week_data][king_data]["報名列表"][user_index]["傷害"]
            await self.取消報名(ctx, king_data, user_index+1, week_data, author_id)
            meme_index = (week - now['周']) * list_refresh_king + king - 1
            """ SignUp_List_tmp = All_OutKnife_Data[week_data][king_data]["報名列表"]
            index_tmp = 0
            for v in SignUp_List_tmp:
                if index_tmp < user_index:
                    print(v['呼叫'])
                    v['呼叫'] += 1
                    index_tmp += 1
                else:
                    break """
        else:
            return 0
        # except:
        #     print(sys.exc_info()[0])
        #     return 0

        # 傷害計算
        now_king_left_hp = All_OutKnife_Data[week_data][king_data]["資訊"]["hp"]
        now_king_left_hp -= damage
        All_OutKnife_Data[week_data][king_data]["資訊"]["hp"] = now_king_left_hp
        await self.meme_edit(ctx, week, king, meme_index)
        if now_king_left_hp > 0:
            return 0

        # 跳下一隻王
        king += 1
        # 清除出刀清單
        tea_fig_cut_out_list_del()
        cut_out_list_index = 7
        meme_index = (week - now['周']) * list_refresh_king + cut_out_list_index - 1
        await self.meme_edit(ctx, week, cut_out_list_index, meme_index)
        change_week_ea = False
        if(king > 5):
            king = 1
            week_tmp = now['force_week']
            week_tmp += 1
            now['force_week'] = week_tmp
            change_week_ea = True
        now['王'] = king
        meme_index = (week - now['周']) * list_refresh_king + king - 1
        force_week = now['force_week']
        king_key = tea_fig_KingIndexToKey(All_OutKnife_Data[week], king)
        All_OutKnife_Data[week][king_key]["資訊"]["hp"] = tea_fig_get_king_hp(
            force_week, king)
        SignUp_List = All_OutKnife_Data[week][king_key]["報名列表"]
        over_id = All_OutKnife_Data[week][king_key]["資訊"]["header"]
        send_msg += f'{force_week}周{king_key}出了'
        try:
            send_msg += f'，{over_id}補償先進去'
        except:
            over_id = ""
        send_msg += f'\n其餘完整刀準備(´﹀`)'

        """ 呼叫、進場判定 """
        overflow_SignUp_List = All_OutKnife_Data[week]["補償清單"]["報名列表"]
        del_list = []
        tmp_index = 1
        for v in SignUp_List:
            if len(tea_fig_list_check(overflow_SignUp_List, v["id"])) > 0:
                continue
            if tmp_index > king_enter_call_max:
                break
            tmp_id = v['id']
            """ if v['呼叫'] == 0:
                tmp_index += 1
                send_msg += f'\n{tmp_id}' """
            if(v['進場']+2 < v['呼叫']):
                del_list.append(v)
            else:
                tmp_index += 1
                send_msg += f'\n{tmp_id}'
            v['呼叫'] += 1
        del_str = ''
        for v in del_list:
            SignUp_List.remove(v)
            del_str += '\n~~' + v['id'] + "~~"
        if del_str != '':
            send_msg += '\n因（進刀次數）<（被叫到的次數)3次，取消報名' + del_str

        await ctx.send(send_msg)
        await self.data輸出(ctx)
        await self.now輸出(ctx)
        await self.now_edit(ctx)
        await self.meme_edit(ctx, week, king_key, meme_index)
        if(change_week_ea):
            await self.清單(ctx, 6)
            # await self.meme_edit(ctx, 'all') #不更新列表
        # channel2 = self.bot.get_channel(tea_fig_channel)
        # await channel2.send(send_msg)

    @commands.command()
    async def 切換王(self, ctx, msg):
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if (admin_check(author_id, self.bot) != True):
            if(limit_enable):
                if (channel_id not in [tea_fig_channel]):
                    return 0
        king = now['王']
        king = int(msg)
        now['王'] = king
        week = now['周']
        tea_fig_cut_out_list_del()
        cut_out_list_index = 7
        meme_index = (week - now['周']) * list_refresh_king + cut_out_list_index - 1
        await self.meme_edit(ctx, week, cut_out_list_index, meme_index)
        await ctx.send(f'切換王成功')
        await self.now輸出(ctx)
        await self.now_edit(ctx)

    """ ----------------- 王數 -----------------"""
    @commands.command()
    async def now(self, ctx):
        week = now['周']
        king = now['王']
        limit = now['limit_max_week']
        await ctx.send(f'周:{week},王:{king},限制周:{limit}')
        # now = {'周': 1, '王': 1, 'limit_max_week':10}
    """ ----------------- admin command -----------------"""
    @commands.command()
    async def now輸出(self, ctx):
        now_save()

    @commands.command()
    async def now_print(self, ctx):
        author_id = ctx.author.id
        ''' 權限 '''
        if(admin_check(author_id, self.bot) != True):
            return 0
        week = now['force_week']
        king = now['王']
        limit_max_week = now['limit_max_week']
        msg = await ctx.send(f'```目前進度, 周:{week}, 王:{king}```')
        now_msg[0] = msg
        now['msg_id'] = msg.id
        await self.now輸出(ctx)
        await self.now_edit(ctx)

    @commands.command()
    async def now_edit(self, ctx):
        week = now['force_week']
        king = now['王']
        limit_max_week = now['limit_max_week']
        content = f'```目前進度, 周:{week}, 王:{king}```'
        await now_msg[0].edit(content=content)

    @commands.command()
    async def data輸出(self, ctx):
        data_save()

    ''' @commands.command()
    async def 新增(self, ctx, msg):
        week = now['周']
        author_id = ctx.author.id

        if(admin_check(author_id,self.bot) == True):
            if not(msg in All_OutKnife_Data[week].keys()):
                All_OutKnife_Data[week][msg] = {
                    "資訊": {"header": "", "footer": "", "hp": 600}, "報名列表": []}
                await ctx.send(f'{msg}新增成功')
            else:
                await ctx.send(f'{msg}新增失敗, 已在列表中')

    @commands.command(name='刪除列表',
                      # description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['clear'],
                      )
    async def 刪除列表(self, ctx, msg):
        week = now['周']
        author_id = ctx.author.id
        if(admin_check(author_id,self.bot) == True):
            msg = tea_fig_KingIndexToKey(All_OutKnife_Data[week], msg)
            All_OutKnife_Data[week][msg]["報名列表"] = []
            await ctx.send(f'{msg} 列表刪除成功')

    @commands.command()
    async def 刪除(self, ctx, msg):

        if(admin_check(author_id,self.bot) == True):
            print(msg)
            week = now['周']
            if(msg.lower == "all"):
                All_OutKnife_Data[week].clear()
                await ctx.send('資料已全數刪除')
            elif(msg in All_OutKnife_Data[week].keys()):
                All_OutKnife_Data[week][msg].clear()
                await ctx.send(f'{msg}刪除成功!')
            else:
                await ctx.send(f'列表中找尋不到X王，刪除失敗ฅ(• 口•)ฅ! ({msg})') '''

    """ @commands.command()
    async def 限制周(self, ctx, msg):
        author_id = ctx.author.id
        if(admin_check(author_id,self.bot) == True):
            now['limit_max_week'] = int(msg)
            await ctx.send(f'限制王成功{msg}周')
            await self.now輸出(ctx)
            await self.now_edit(ctx) """

    @commands.command()
    async def show_限制周(self, ctx):
        author_id = ctx.author.id
        if(admin_check(author_id, self.bot) == True):
            week = now['limit_max_week']
            await ctx.send(f'限制周:{week}周')

    @commands.command(ame='血量變更',
                      brief="Answers from the beyond.",
                      aliases=['ch'],
                      )
    async def 血量變更(self, ctx, msg):
        author_id = ctx.author.id
        if(admin_check(author_id, self.bot) != True):
            return 0
        week = now["周"]
        force_week = now["force_week"]
        king = now['王']
        king_key = tea_fig_KingIndexToKey(All_OutKnife_Data[1], king)
        All_OutKnife_Data[week][king_key]["資訊"]["hp"] = int(msg)
        await ctx.send(f'{force_week}周{king_key}血量變更成功!')
        meme_index = (week - now['周']) * list_refresh_king + king - 1
        await self.meme_edit(ctx, week, king_key, meme_index)

    @commands.command()
    async def reset_team_fight_list(self, ctx, msg):
        author_id = ctx.author.id
        overflow_tmp = {'資訊': {"header": "",
                               "footer": "", "hp": 90}, '報名列表': []}
        if(admin_check(author_id, self.bot) == True):
            All_OutKnife_Data.clear()
            for i in range(1, int(msg)+1):
                All_OutKnife_Data[i] = {'1王': {'資訊': {"header": "", "footer": "", "hp": 600}, '報名列表': []},
                                        '2王': {'資訊': {"header": "", "footer": "", "hp": 800}, '報名列表': []},
                                        '3王': {'資訊': {"header": "", "footer": "", "hp": 1000}, '報名列表': []},
                                        '4王': {'資訊': {"header": "", "footer": "", "hp": 1200}, '報名列表': []},
                                        '5王': {'資訊': {"header": "", "footer": "", "hp": 1500}, '報名列表': []}}

                All_OutKnife_Data[i]['補償清單'] = overflow_tmp
                All_OutKnife_Data[i]['出刀清單'] = ReportDamage
            await self.data輸出(ctx)

    @commands.command()
    async def add_team_fight_list(self, ctx, msg1, msg2):
        author_id = ctx.author.id
        if(admin_check(author_id, self.bot) == True):
            for i in range(int(msg1), int(msg2)+1):
                All_OutKnife_Data[i]['補償清單'] = overflow
                All_OutKnife_Data[i]['出刀清單'] = ReportDamage
                ''' All_OutKnife_Data[i] = {'1王': {'資訊': {"header": "", "footer": "", "hp": 600}, '報名列表': []},
                                '2王': {'資訊': {"header": "", "footer": "", "hp": 800}, '報名列表': []},
                                '3王': {'資訊': {"header": "", "footer": "", "hp": 1000}, '報名列表': []},
                                '4王': {'資訊': {"header": "", "footer": "", "hp": 1200}, '報名列表': []},
                                '5王': {'資訊': {"header": "", "footer": "", "hp": 1500}, '報名列表': []}}  '''

    """----------------- admin command -----------------"""

    """----------------- meme command -----------------"""
    @commands.Cog.listener()
    async def on_message(self, msg):
        channel_id = msg.channel.id
        ''' 權限 '''
        if(channel_id == only_meme_speak_channel):
            if(msg.author != self.bot.user):
                # print(msg)
                await msg.delete(delay=3)

    @commands.command()
    async def meme_del(self, ctx, msg):
        msg = int(msg)
        channel = self.bot.get_channel(only_meme_speak_channel)
        tmp = []
        tmp.append(list_msg_tmp[msg][2])
        del list_msg_tmp[msg]
        await channel.delete_messages(tmp)

    @commands.command()
    async def meme_edit(self, ctx, *msg):
        if(msg[0] == 'all'):
            # print('meme_edit all')
            now_week = now['周']
            now_king = 1
            for i in range(0, list_refresh_max_index):
                # try:
                if(i in bypass_list_index):
                    continue
                # print("i",i,int(i / 6), int(i % 6))
                week = int(i / list_refresh_king) + now_week
                king = int(i % list_refresh_king) + now_king

                # print("周王",week, king)
                # print(list_msg_tmp[i][2].id)
                re = tea_fig_list_func([king, week])
                list_msg_tmp[i][0] = week
                list_msg_tmp[i][1] = tea_fig_KingIndexToKey(
                    All_OutKnife_Data[1], king)
                await list_msg_tmp[i][2].edit(embed=re[1])
                # except:
                # print(f'{week} {king} msg not find')

        else:
            # print(msg)
            week = msg[0]
            king = msg[1]
            """ if(king == 6):
                i = 17
            else: """
            i = msg[2]
            re = tea_fig_list_func([king, week])
            await list_msg_tmp[i][2].edit(embed=re[1])

    @commands.command()
    async def meme_test(self, ctx):
        # tmp = tea_fig_list_func( [1])
        print(len(list_msg_tmp))

    """----------------- meme command -----------------"""

    """----------------- reaction command -----------------"""
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        force_week = now['force_week']
        # mes_id = payload.message_id
        user_id = payload.user_id
        channel_id = payload.channel_id
        channel = self.bot.get_channel(channel_id)

        # print( emoji_id + "123")
        # print(user_id, self.bot.user)

        if (channel_id == only_meme_speak_channel) and (user_id != robot_id):
            emoji_id = payload.emoji
            if(str(emoji_id) == sign_up_emoji):

                try:
                    if(any(user_id in [number_insert_msg[tmp][0]] for tmp in number_insert_msg)):
                        await channel.send(f'<@!{user_id}>你先前報名的尚未輸入完畢喔(3秒後清除)', delete_after=3)
                        return 0
                except:
                    print("檢查失敗")
                # try:
                msg_index = [
                    msg_index for msg_index in list_msg_tmp if payload.message_id in [msg_index[2].id]][0]
                week = msg_index[0]
                king = tea_fig_KingIndexToKey(
                    All_OutKnife_Data[1], msg_index[1])
                SignUp_List = All_OutKnife_Data[week][king]["報名列表"]
                if(len(tea_fig_list_check(SignUp_List, f'<@!{user_id}>')) >= list_max_enter):
                    await channel.send(f'<@!{user_id}>報名失敗, 已在列表中或超過上限(最多1筆)(3秒後清除)', delete_after=3)
                    return 0

                # print(week, king)
                if(king == '補償清單'):
                    # await channel.send(f'<@!{user_id}>你準備報名{king} (3秒後清除)', delete_after=3)
                    await self.enter_to_overflow_list_from_emoji(channel, user_id, week, king)
                elif(king == '出刀清單'):
                    return 0
                else:
                    # await channel.send(f'<@!{user_id}>你準備報名{force_week}周{king} (3秒後清除)', delete_after=3)
                    await self.enter_to_king_from_emoji(channel, user_id, week, king)
                """ except:
                    print('emoji報名失敗') """
            if(str(emoji_id) == cancel_emoji):
                # try:
                msg_index = [
                    msg_index for msg_index in list_msg_tmp if payload.message_id in [msg_index[2].id]][0]
                week = msg_index[0]
                king = tea_fig_KingIndexToKey(
                    All_OutKnife_Data[1], msg_index[1])
                if(len(All_OutKnife_Data[week][king]['報名列表']) > 0):
                    used_list = [tmp['id']
                                 for tmp in All_OutKnife_Data[week][king]['報名列表']]
                    try:
                        user_index = used_list.index(f'<@!{user_id}>')
                        await self.取消報名(channel, king, user_index+1, week, user_id)
                    except:
                        # await channel.send(f'<@!{user_id}>還想搞事啊 取消你媽逼')
                        return 0

                ''' except:
                    pass '''
            if(str(emoji_id) == overflow_emoji):
                # print('overflow emoji')
                try:
                    if(any(user_id in [number_insert_msg[tmp][0]] for tmp in number_insert_msg)):
                        await channel.send(f'<@!{user_id}>你先前報名的尚未輸入完畢喔(3秒後清除)', delete_after=3)
                        return 0
                except:
                    pass
                msg_index = [
                    msg_index for msg_index in list_msg_tmp if payload.message_id in [msg_index[2].id]][0]
                week = msg_index[0]
                king = tea_fig_KingIndexToKey(
                    All_OutKnife_Data[1], msg_index[1])
                if(king in ['補償清單', '出刀清單']):
                    return 0
                await channel.send(f'<@!{user_id}>你準備報名{king}補償刀 (3秒後清除)', delete_after=3)
                await self.enter_to_overflow_from_emoji(channel, user_id, week, king)
            if(str(emoji_id) == overflow_cancel_emoji):
                # print('overflow cancel emoji')
                msg_index = [
                    msg_index for msg_index in list_msg_tmp if payload.message_id in [msg_index[2].id]][0]
                week = msg_index[0]
                king = tea_fig_KingIndexToKey(
                    All_OutKnife_Data[1], msg_index[1])
                try:
                    await self.取消補償刀(channel, king, week, user_id)
                except:
                    return 0

            try:
                if(user_id != number_insert_msg[payload.message_id][0]):
                    return 0
            except:
                return 0
            # try:
            content = event_number_insert(payload)
            if(content == 'enter'):
                msg = number_insert_msg[payload.message_id][3]
                week = number_insert_msg[payload.message_id][1]
                king = number_insert_msg[payload.message_id][2]

                if(king == "補償清單"):
                    default_content = msg.content.split(':', 1)[0]
                    info = msg.content.split(':', 1)[1]
                    if(default_content.find('請輸入秒數') != -1):
                        default_content = default_content.replace(
                            '請輸入秒數', f'請輸入(1~5)王{info}秒')
                        # print(default_content)
                        await number_insert_msg[payload.message_id][3].edit(content=f'{default_content}:')
                    else:
                        insert_sec = default_content.split('(1~5)王', 1)[1]
                        insert_sec = insert_sec[:-5]
                        # print(insert_sec, info)
                        await number_insert_msg[payload.message_id][3].delete()
                        del number_insert_msg[payload.message_id]
                        await self.報名(channel, king, insert_sec, info, user_id)
                elif(king == "出刀清單"):
                    pass
                else:
                    default_content = msg.content.split(':', 1)[0]
                    info = msg.content.split(':', 1)[1]
                    if(default_content.find('補償刀') != -1):
                        await number_insert_msg[payload.message_id][3].delete()
                        del number_insert_msg[payload.message_id]
                        await self.補償(channel, king, info, week, user_id)
                    else:
                        await number_insert_msg[payload.message_id][3].delete()
                        del number_insert_msg[payload.message_id]
                        await self.報名(channel, king, info, week, user_id)
            elif(content):
                await number_insert_msg[payload.message_id][3].edit(content=content)
            else:
                pass
            """except:
                pass"""
            # await channel.send(f'<@!{user_id}>你為什麼偷偷關注我，你是不是喜歡人家٩( >ω< )وو{emoji_id} (3秒後清除)', delete_after=3)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # mes_id = payload.message_id
        user_id = payload.user_id
        channel_id = payload.channel_id
        channel = self.bot.get_channel(channel_id)
        emoji_id = payload.emoji
        if channel_id == only_meme_speak_channel and (user_id != robot_id):
            try:
                if(user_id != number_insert_msg[payload.message_id][0]):
                    return 0
            except:
                return 0
            content = event_number_insert(payload)
            if(content == 'enter'):
                pass
            elif(content):
                await number_insert_msg[payload.message_id][3].edit(content=content)
            else:
                pass
            # await channel.send(f'<@!{user_id}>不~~~ 不要離開我(๑•́︿•̀๑){emoji_id} (3秒後清除)', delete_after=3)

    @commands.command()
    async def enter_to_king_from_emoji(self, ctx, user_id, week, king):
        force_week = now['force_week']
        msg = await ctx.send(f'<@!{user_id}>請輸入傷害{force_week}周{king}:')
        number_insert_msg[msg.id] = [user_id, week, king, msg]
        reactions = number_emoji
        for emoji in reactions:
            await msg.add_reaction(emoji)

    @commands.command()
    async def enter_to_overflow_list_from_emoji(self, ctx, user_id, week, king):
        msg = await ctx.send(f'<@!{user_id}>請輸入秒數{king}:')
        number_insert_msg[msg.id] = [user_id, week, king, msg]
        reactions = number_emoji
        for emoji in reactions:
            await msg.add_reaction(emoji)

    @commands.command()
    async def enter_to_overflow_from_emoji(self, ctx, user_id, week, king):
        msg = await ctx.send(f'<@!{user_id}>請輸入秒數{king}補償刀:')
        number_insert_msg[msg.id] = [user_id, week, king, msg]
        reactions = number_emoji
        for emoji in reactions:
            await msg.add_reaction(emoji)
    """----------------- reaction command -----------------"""
    ''' [692739940282531883, 692739944686551133, 692739950994522224, 692739955620839504, 692739960910118962, 0, 692739964936519681, 692739970129199206, 692739974583418991, 692739979792613466, 692739984649748521, 0, 692739989125201970, 692739994586185778, 692739998717444188, 692740003989684344, 692740008809070632, 692740013666074685] '''

    @commands.command(name='test',
                      description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['t'])
    async def test(self, ctx):
        print(list_msg_tmp_id)
        for i in list_msg_tmp:
            print(i[0], i[1])
        print(All_OutKnife_Data[1]["出刀清單"]["報名列表"])
        pass
        # print(overflow)
        # print(All_OutKnife_Data)
        #
        # print(msg.id)
        # await ss.edit("test")
        # number_insert_msg.clear()
        # list_msg_tmp.clear()

    @commands.command(aliases=['p'])
    async def 清單_print(self, ctx, *msg):

        list_msg_tmp.clear()
        if(len(list_msg_tmp) >= list_refresh_max_index):
            list_msg_tmp.clear()
        channel_id = ctx.channel.id
        author_id = ctx.author.id
        ''' 權限 '''
        if(admin_check(author_id, self.bot) != True):
            if (channel_id != tea_fig_channel):
                return 0
        """ try: """
        try:
            week = int(msg[1])
        except:
            week = now['周']
        tmp_king = []
        if(msg[0] == 'all'):
            for k in All_OutKnife_Data[week]:
                tmp_king.append(k)
        else:
            tmp_king.append(msg[0])

        msg_week = msg[1]
        tmp_index = 0
        for w_add in range(0, list_refresh_week):
            for k in tmp_king:
                if (tmp_index in bypass_list_index):
                    list_msg_tmp.append([0, 0, list_msg_empty()])
                    continue
                number_insert_msg = [k, week]
                tmp = tea_fig_list_func(number_insert_msg)
                s_msg = await ctx.send(embed=tmp[1])
                if(k != '出刀清單'):
                    await s_msg.add_reaction(sign_up_emoji)
                    await s_msg.add_reaction(cancel_emoji)
                # if(k != '補償清單'):
                #     await s_msg.add_reaction(overflow_emoji)
                #     await s_msg.add_reaction(overflow_cancel_emoji)
                if(len(list_msg_tmp) < list_refresh_max_index):
                    list_msg_tmp.append([week, k, s_msg])
                    # print(week, k, len(list_msg_tmp))
                tmp_index += 1
            week += 1

        tmp = []
        for id in list_msg_tmp:
            # print(id)
            tmp.append(id[2].id)
        f = open("./data/list_msg_tmp.json", "w")
        f.write(f'{json.dumps(tmp)}')
        f.close()
        """ except:
            await ctx.send("```arm\n欲查詢列表請標注特定王(ฅฅ*)\n``` ex. \*列表 all ,\*列表 ?王")
            print(sys.exc_info()[0]) """


def setup(bot):
    bot.add_cog(Team_Fight(bot))


def tea_fig_list_check(matrix, author_str):
    """ 確認人員在列表內，回傳index列表 """
    result = []
    index = 0
    for v in matrix:
        """ print(v)
        print(f'<@!{author_id}>')  """
        if(v["id"] == f'{author_str}'):
            result.append(index)
        index += 1
    return result


def tea_fig_error_message():
    return "指令錯誤,輸入[*help 指令]了解詳情"


def tea_fig_PlusAllDamage(SignUp_List, in_id=-1):
    all_dam = 0
    n = 1
    for v in SignUp_List:
        # print(v)
        if(n != in_id):
            all_dam += int(v["傷害"])
        n += 1
    return all_dam


def tea_fig_DamageCheck(SignUp_List, damage_in, king_hp, author_id, in_id=-1):
    # 去除傷害檢測
    """ if (damage_in < 99):
        return False, f'<@!{author_id}>預估傷害輸入錯誤(100-999),少輸入一位數了呦，再檢查看看( •́ㅿ•̀ )'
    elif (damage_in > 999):
        return False, f'<@!{author_id}>預估傷害輸入錯誤(100-999),超出傷害上限了呦( •́ㅿ•̀ )'
    if(tea_fig_PlusAllDamage(SignUp_List, in_id) >= king_hp):
        return False, f'<@!{author_id}>預估傷害超過王總血量,總傷害已經爆表拉( •́ㅿ•̀ )' """
    return 1, ""


''' def tea_fig_new_week():
    new_OutKnife_Data = {'1王': {'資訊': {"header": "", "footer": "", "hp": 600}, '報名列表': []},
                         '2王': {'資訊': {"header": "", "footer": "", "hp": 800}, '報名列表': []},
                         '3王': {'資訊': {"header": "", "footer": "", "hp": 1000}, '報名列表': []},
                         '4王': {'資訊': {"header": "", "footer": "", "hp": 1200}, '報名列表': []},
                         '5王': {'資訊': {"header": "", "footer": "", "hp": 1500}, '報名列表': []}}

    new_OutKnife_Data['補償清單'] = All_OutKnife_Data[week]['補償清單']
    return new_OutKnife_Data '''


def tea_fig_list_func(msg):
    """ 回傳清單embed """
    try:
        week = int(msg[1])
    except:
        week = now['周']
    msg = msg[0]
    img_url = ""
    unit = ""
    embed_color = 0
    week_str = f'```{week}周```'
    king = now['王']
    king_str = f'```{king}王```'
    try:
        msg = int(msg)
        king_index = msg
        king_key_list_tmp = list(All_OutKnife_Data[week].keys())
        msg = king_key_list_tmp[msg-1]
    except:
        msg = msg
        king_index = list(All_OutKnife_Data[week].keys()).index(msg) + 1
    SignUp_List = All_OutKnife_Data[week][msg]["報名列表"]
    img_url = img_url_list[msg]
    unit = unit_list[msg]
    if(msg not in ["補償清單", "出刀清單"]):
        # f'{All_OutKnife_Data[week][msg]["資訊"]["hp"]}'
        damage_info = f'{tea_fig_get_king_hp(now["force_week"], king_index)}'
        left_hp = f'{All_OutKnife_Data[week][msg]["資訊"]["hp"]}'
        header_info = All_OutKnife_Data[week][msg]["資訊"]["header"]
        # remaining = 1  # int(damage_info) - tea_fig_PlusAllDamage(SignUp_List)
        # if(remaining > 0):
        footer_info = f'預估剩餘血量:{left_hp}{unit}'
        if(header_info == ""):
            embed_color = embed_color_list["可報_無補"]
        else:
            embed_color = embed_color_list["可報_有補"]
        # elif(remaining <= 0):
        #     footer_info = ""  # f'預估剩餘:{remaining}{unit}, 報名已截止'
        #     embed_color = embed_color_list["不可報"]
        set_author_name = f'{msg} {damage_info}{unit}'
    elif(msg == "補償清單"):
        damage_info = ""
        header_info = ""
        footer_info = '補償丟出去後記得使用指令刪除(๑•᎑•๑)'
        embed_color = embed_color_list["補償清單"]
        set_author_name = f'{msg} {damage_info}'
    elif(msg == "出刀清單"):
        damage_info = ""
        header_info = ""
        footer_info = '換王後會自動清除喔(๑•᎑•๑)'
        embed_color = embed_color_list["出刀清單"]
        set_author_name = f'{msg} {damage_info}'

    """ embed 產生 """
    embed = discord.Embed(
        title=' ', description=header_info, color=0xaae3aa)
    embed.set_author(name=set_author_name, icon_url=img_url)
    # embed.set_thumbnail(url=)
    n = 1
    for k2 in SignUp_List:
        remark = "- " + k2["備註"] if "備註" in k2 else ''
        tree = "[掛樹]" if "tree" in k2 else ''
        if(msg == "補償清單"):
            embed.add_field(
                name=f'No.{n}', value=f'{k2["id"]} {k2["傷害"]}{unit}', inline=False)
        elif(msg == "出刀清單"):
            embed.add_field(
                name=f'No.{n}{tree}', value=f'{k2["id"]} {k2["傷害"]}{unit}{remark}', inline=False)
        else:
            embed.add_field(
                name=f'No.{n}', value=f'{k2["id"]} {k2["傷害"]}{unit},{k2["呼叫"]},{k2["進場"]}', inline=False)
        n = n+1
    embed.set_footer(text=footer_info)
    # await ctx.send(f'```{week}周```')
    return [f'{week_str}', embed]


def tea_fig_get_king_hp(week, king):
    """ 清單總血量獲取(hp) """
    hp = 0
    for i in king_hp_default:
        mt = False
        lt = False
        if i[0]:
            if week >= i[0]:
                mt = True
        else:
            mt = True
        if i[1]:
            if week <= i[1]:
                lt = True
        else:
            lt = True
         # print(mt, lt, week, i)
        if mt and lt:
            hp = i[king+1]
            break
    return hp


def tea_fig_enter_info_change(SignUp_List, id, info):
    """ 更改報名資訊，多筆更改第一筆 """
    index = tea_fig_list_check(SignUp_List, f'<@!{id}>')
    if(len(index) > 0):
        for k in info:
            SignUp_List[index[0]][k] = info[k]
            data_save()
        return True
    return False


def tea_fig_cut_out_list_sort():
    week = now['周']
    king = tea_fig_KingIndexToKey(All_OutKnife_Data[1], now['王'])
    overflow_SignUp_List = All_OutKnife_Data[week][king]['報名列表']
    cut_out_SignUp_List = All_OutKnife_Data[week]['出刀清單']['報名列表']
    index = 0
    for record in overflow_SignUp_List:
        cut_out_index = tea_fig_list_check(cut_out_SignUp_List, record['id'])
        if len(cut_out_index) > 0:
            cut_out_SignUp_List[cut_out_index[0]]['index'] = index
            index += 1
    All_OutKnife_Data[week]['出刀清單']['報名列表'] = sorted(
        cut_out_SignUp_List, key=lambda x: x['index'] if 'index' in x else 999)


def tea_fig_cut_out_list_del():
    week = now['周']
    cut_out_SignUp_List = All_OutKnife_Data[week]['出刀清單']['報名列表']
    cut_out_SignUp_List.clear()


def event_number_insert(payload):
    """ 按鍵數字輸入 """
    emoji_id = payload.emoji
    try:
        number_index = number_emoji.index(str(emoji_id))
    except:
        return False
    if(number_insert_msg[payload.message_id][0] != payload.user_id):
        return False
    msg = number_insert_msg[payload.message_id][3]
    if(payload.message_id == number_insert_msg[payload.message_id][3].id):
        tmp = f'{msg.content}'
        tmp = tmp.split(':', 1)
        default_content = tmp[0]
        old_content = tmp[1]
        if(number_index == 10):
            content = old_content[:-
                                  1]if len(old_content) > 0 else old_content
        elif(number_index == 11):
            # print("enter")
            return 'enter'
        else:
            content = f'{old_content}{number_index}'
        return f'{default_content}:{content}'
