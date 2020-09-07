# coding=UTF-8
import random
import discord
from discord.ext import commands
import json
import os
from model.func import *
#import keep_alive
import re

bot = commands.Bot(
    command_prefix=setting_data['BOT_PREFIX'], case_insensitive=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    ''' channel object '''

    if team_fight_function_enable and team_fight_list_compare_enable:
        meme_channel_obj = bot.get_channel(meme_channel)
        only_meme_speak_channel_obj = bot.get_channel(only_meme_speak_channel)
        run_channel = bot.get_channel(run_out_before_look)
        backup_channel = bot.get_channel(backup_channel_id)

        await backup_channel.send(content=f'系統斷線重啟')
        msg_tip = []
        change_content_list = []  # if system changed save there
        msg_tip.append(await run_channel.send(content=f'系統斷線重啟，資料核對中，請勿操作'))

        ''' now message object '''
        # [now] get data
        msg_tip.append(await run_channel.send(content=f'周,王 核對開始'))
        try:
            now_msg[0] = await only_meme_speak_channel_obj.fetch_message(now['msg_id'])
            now_tmp = now_msg[0].content.replace('```', '')  # get message
            week_dc = int(now_tmp.split('周:')[1].split(',')[0])
            king_dc = int(now_tmp.split('王:')[1].split(',')[0])
            #limit_dc = int(now_tmp.split('限制周:')[1].split(',')[0])
            msg_tip.append(await run_channel.send(content=f'目前進度, 周:{week_dc}, 王:{king_dc}'))
            week_sys = int(now['force_week'])
            king_sys = int(now['王'])
            limit_sys = int(now['limit_max_week'])
            msg_tip.append(await run_channel.send(content=f'系統進度, 周:{week_sys}, 王:{king_sys}'))

            # [now] compare data
            now_changed_content = ''
            #week_tmp = week_dc - int(now['周'])
            if (week_dc != week_sys):
                now['force_week'] = week_dc
                now_changed_content += f'```arm\n周:{week_sys} -> {week_dc}\n```'
            #king_tmp = king_dc - int(now['王'])
            if (king_dc != king_sys):
                now['王'] = king_dc
                now_changed_content += f'```arm\n王:{king_sys} -> {king_dc}\n```'
            #limit_tmp = limit_dc - int(now['limit_max_week'])
            """ if (limit_dc != limit_sys):
                now['limit_max_week'] = limit_dc
                now_changed_content += f'```arm\n限制周:{limit_sys} -> {limit_dc}\n```' """
            if(now_changed_content):
                #print (now_changed_content)
                change_content_list.append(now_changed_content)
                #await run_channel.send(content=now_changed_content)
                now_save()
            msg_tip.append(await run_channel.send(content=f'周,王 核對完畢'))
        except:
            error = f'周,王 核對失敗，資料可能遺失'
            await run_channel.send(content=error)
            await backup_channel.send(content=error)

        # [now] backup data
        if(now_changed_content):
            msg_tip.append(await run_channel.send(content=f'資料有更動，備份中'))
            await backup_channel.send(content=now_changed_content)
            msg_tip.append(await run_channel.send(content=f'備份完成'))

        ''' list message object '''
        # [list] get data
        msg_tip.append(await run_channel.send(content=f'報名清單 核對開始'))
        msg_obj_list = []
        for id in list_msg_tmp_id:
            # print(id) # message id
            if id == 0:
                msg_obj = list_msg_empty()
            else:
                msg_obj = await only_meme_speak_channel_obj.fetch_message(id)
                msg_obj_list.append(msg_obj)
            list_msg_tmp.append([0, 0, msg_obj])

        # try:
        # [list] compare data
        oo_week_wmp = 0
        for msg_obj in msg_obj_list:
            list_changed_content = ''
            msg_embeds = msg_obj.embeds
            """ week_tmp = msg_obj.content.replace('```', '')
            week_tmp = int(re.findall("[0-9]+", week_tmp)[0]) """
            week_tmp = 1
            # print(week_tmp)
            if(oo_week_wmp != week_tmp):
                # msg_tip.append(await run_channel.send(content=f'{week_tmp}周'))
                oo_week_wmp = week_tmp
            for i in msg_embeds:
                king_tmp = i.author.name.split(' ')[0]
                # print(king_tmp) #i.author.name 王,hp
                sys_list_tmp = All_OutKnife_Data[week_tmp][king_tmp]['報名列表']
                sys_list_len = len(sys_list_tmp)
                # print(sys_list_len)
                no = 0
                # header
                dc_description = i.description
                sys_description = All_OutKnife_Data[week_tmp][king_tmp]['資訊']['header']
                #print(dc_description, sys_description)
                if(str(dc_description) != str(sys_description)) and (dc_description != discord.Embed.Empty):
                    list_changed_content += f'```arm\n{week_tmp}周{king_tmp} 補償刀:{sys_description} -> {dc_description}\n```'
                    All_OutKnife_Data[week_tmp][king_tmp]['資訊']['header'] = dc_description
                # hp
                if king_tmp not in ['補償清單', '出刀清單']:
                    dc_footer = i.footer.text
                    # print(dc_footer)
                    dc_hp = dc_footer.split(':')[1].replace('W', '')
                    sys_hp = All_OutKnife_Data[week_tmp][king_tmp]['資訊']['hp']
                    #print(dc_hp, sys_hp)
                    if(int(dc_hp) != int(sys_hp)):
                        list_changed_content += f'```arm\n{week_tmp}周{king_tmp} 剩餘血量:{sys_hp} -> {dc_hp}\n```'
                        All_OutKnife_Data[week_tmp][king_tmp]['資訊']['hp'] = int(
                            dc_hp)

                # 報名列表
                while(len(i.fields) < sys_list_len):
                    sys_list_tmp.pop()
                    sys_list_len -= 1
                for i2 in i.fields:
                    tmp = i2.value.split(' ', 1)
                    dc_id = tmp[0]
                    all_str = tmp[1].split('-',1)
                    dc_damage = all_str[0].replace('W', '').replace('S', '')
                    tmp_tmp = dc_damage.split(',')
                    king_kill_index = int(tmp_tmp[1]) if len(tmp_tmp) > 1 else 0
                    cut_out_index = int(tmp_tmp[2]) if len(tmp_tmp) > 2 else 0
                    remark = all_str[1] if len(all_str) > 1 else False
                    dc_damage = tmp_tmp[0]

                    # print(dc_id,dc_damage)
                    if(no < sys_list_len):
                        sys_id = sys_list_tmp[no]['id']
                        sys_damage = sys_list_tmp[no]['傷害']
                        # print(sys_id,sys_damage)
                        if (str(dc_id) != str(sys_id)) or (str(dc_damage) != str(sys_damage)):
                            list_changed_content += f'```arm\n{week_tmp}周{king_tmp} no.{no+1} id:{sys_id} -> {dc_id} info:{sys_damage} -> {dc_damage}\n```'
                            sys_list_tmp[no]['id'] = dc_id
                            sys_list_tmp[no]['傷害'] = dc_damage
                    else:
                        list_changed_content += f'```arm\n{week_tmp}周{king_tmp} no.{no+1} id: -> {dc_id} info: -> {dc_damage}\n```'
                        l = len(sys_list_tmp)
                        try:
                            dc_damage = int(dc_damage)
                        except:
                            pass
                        sys_list_tmp.insert(
                            l, {"id": dc_id, "傷害": dc_damage, "呼叫": king_kill_index, "進場": cut_out_index})
                        if remark:
                            sys_list_tmp[l]["備註"] = remark
                    no += 1
            if(list_changed_content):
                change_content_list.append(list_changed_content)
                #await run_channel.send(content=list_changed_content)
                # [list] backup data
                msg_tip.append(await run_channel.send(content=f'資料有更動，備份中'))
                await backup_channel.send(content=list_changed_content)
                msg_tip.append(await run_channel.send(content=f'備份完成'))
        data_save()
        now_save()
        msg_tip.append(await run_channel.send(content=f'報名清單 核對完畢'))
        """ except:
            error = f'報名清單 核對失敗，資料可能遺失'
            await run_channel.send(content=error)
            await backup_channel.send(content=error) """

        # [list] update list_msg_tmp
        msg_tip.append(await run_channel.send(content=f'資料同步開始'))
        now_week = now['周']
        now_king = 1
        for i in range(0, list_refresh_max_index):
            if(i in bypass_list_index):
                continue
            #print("i",i,int(i / 6), int(i % 6))
            week = int(i / list_refresh_king) + now_week
            king = int(i % list_refresh_king) + now_king
            #print("周王",week, king)
            # print(list_msg_tmp[i][2].id)
            list_msg_tmp[i][0] = week
            list_msg_tmp[i][1] = tea_fig_KingIndexToKey(
                All_OutKnife_Data[1], king)
        msg_tip.append(await run_channel.send(content=f'資料同步完畢'))
        msg_tip.append(await run_channel.send(content=f'系統重啟完成!(5秒後清除)'))
        ''' delete message '''
        for i in msg_tip:
            await i.delete(delay=5)

        await backup_channel.send(content=f'系統重啟完成!')

    ''' list message object (測試用)'''
    # [list] get data
    if not team_fight_list_compare_enable and team_fight_function_enable:
        meme_channel_obj = bot.get_channel(meme_channel)
        only_meme_speak_channel_obj = bot.get_channel(only_meme_speak_channel)
        run_channel = bot.get_channel(run_out_before_look)
        backup_channel = bot.get_channel(backup_channel_id)
        msg_obj_list = []
        now_msg[0] = await only_meme_speak_channel_obj.fetch_message(now['msg_id'])
        for id in list_msg_tmp_id:
            # print(id) # message id
            if id == 0:
                msg_obj = list_msg_empty()
            else:
                msg_obj = await only_meme_speak_channel_obj.fetch_message(id)
                msg_obj_list.append(msg_obj)
            list_msg_tmp.append([0, 0, msg_obj])
        now_week = now['周']
        now_king = 1
        for i in range(0, list_refresh_max_index):
            if(i in bypass_list_index):
                continue
            #print("i",i,int(i / 6), int(i % 6))
            week = int(i / list_refresh_king) + now_week
            king = int(i % list_refresh_king) + now_king
            #print("周王",week, king)
            # print(list_msg_tmp[i][2].id)
            list_msg_tmp[i][0] = week
            list_msg_tmp[i][1] = tea_fig_KingIndexToKey(
                All_OutKnife_Data[1], king)
    print('------')


@bot.event
async def on_resumed():
    print('embed_color_list')


@bot.command()
async def load(ctx, extension):
    author_id = ctx.author.id
    if(admin_check(author_id) == True):
        bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'Loaded {extension}')


@bot.command()
async def unload(ctx, extension):
    author_id = ctx.author.id
    if(admin_check(author_id) == True):
        bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'Unloaded {extension}')


@bot.command()
async def reload(ctx, extension):
    author_id = ctx.author.id
    if(admin_check(author_id) == True):
        bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Reloaded {extension}')

# help ending note
""" bot.help_command.get_ending_note """

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        if not team_fight_function_enable:
            if filename == 'team_fight.py':
                continue
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    #keep_alive.keep_alive()
    bot.run(setting_data['TOKEN'])
