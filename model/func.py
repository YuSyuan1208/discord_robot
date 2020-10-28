import json
import ast

with open('./data/setting.json', 'r', encoding='utf8') as jfile:
    setting_data = json.load(jfile)
with open('./data/reply_cmds.json', 'r', encoding='utf8') as jfile:
    reply_data = json.load(jfile)

""" --------------- Initial Parameter --------------- """
# React
react_data = {}

all_function_enable = False  # 未使用
team_fight_list_compare_enable = True  # 重啟清單比對功能
team_fight_function_enable = True  # 戰隊站功能
limit_enable = True  # 指令權限
if team_fight_function_enable:
    robot_id = setting_data['robot_id']  # robot自己的id代碼
    meme_channel = setting_data['meme_channel']  # 測試訊息用頻道
    # 限制team_fight指令觸發頻道(舊)無用
    tea_fig_channel = setting_data['tea_fig_channel']
    # 限制team_fight指令觸發頻道(新)，且發送清單更新資訊
    run_out_before_look = setting_data['run_out_before_look']
    backup_channel_id = setting_data['backup_channel_id']  # 備份頻道
    only_meme_speak_channel = setting_data['only_meme_speak_channel']  # 清單頻道
    list_refresh_week = 1  # 清單列表的循環次數(周)
    list_refresh_king = 7  # 一次清單列表產生的表單數
    list_refresh_max_index = list_refresh_king * list_refresh_week  # 表單總數
    king_enter_call_max = 3  # 呼叫的打手的數目
    bypass_list_index = []  # 不顯示的表單ID
    list_max_enter = 1  # 單張清單最多可報名次數
""" --------------- Initial Parameter --------------- """

""" --------------- Initial Data --------------- """
if team_fight_function_enable:
    All_OutKnife_Data = {}
    now = {'周': 1, '王': 1, 'limit_max_week': 10, 'force_week': 1}
    list_msg_tmp = []  # [week, king, msg]
    now_msg = {}
    number_insert_msg = {}  # [msg.id] = [user_id, week, king, msg]
    king_hp_default = [[1, 10, 600, 800, 1000, 1200, 1500], [
        11, 34, 700, 900, 1300, 1500, 2000], [35, False, 1500, 1600, 1800, 1900, 2000]]
""" --------------- Initial Data --------------- """

""" --------------- Getting Data --------------- """
if team_fight_function_enable:
    with open('./data/data.json', 'r') as content_file:
        All_OutKnife_save_data = content_file.read()
    All_OutKnife_Data = ast.literal_eval(All_OutKnife_save_data)
    overflow = All_OutKnife_Data[1]["補償清單"]
    ReportDamage = All_OutKnife_Data[1]["出刀清單"]

    with open('./data/now_data.json', 'r') as content_file:
        now_save_data = content_file.read()
    now = ast.literal_eval(now_save_data)

    with open('./data/list_msg_tmp.json', 'r') as content_file:
        list_msg_tmp_id_save_data = content_file.read()
    list_msg_tmp_id = ast.literal_eval(list_msg_tmp_id_save_data)

    """ with open('./data/team_fight_setting.json', 'r') as content_file:
        team_fight_setting_save_data = content_file.read()
    team_fight_setting = ast.literal_eval(team_fight_setting_save_data) """

    for i in range(1, len(All_OutKnife_Data)+1):
        """ All_OutKnife_Data[i] = {'1王': {'資訊': {"header": "", "footer": "", "hp": 600}, '報名列表': []},
                                '2王': {'資訊': {"header": "", "footer": "", "hp": 800}, '報名列表': []},
                                '3王': {'資訊': {"header": "", "footer": "", "hp": 1000}, '報名列表': []},
                                '4王': {'資訊': {"header": "", "footer": "", "hp": 1200}, '報名列表': []},
                                '5王': {'資訊': {"header": "", "footer": "", "hp": 1500}, '報名列表': []}}
        overflow = {'資訊': {"header": "", "footer": "", "hp": 90}, '報名列表': []}"""
        #ReportDamage = {'資訊': {"header": "", "footer": "", "hp": 90}, '報名列表': []}
        All_OutKnife_Data[i]['補償清單'] = overflow
        All_OutKnife_Data[i]['出刀清單'] = ReportDamage

    """ team_fight_setting = {'img_url_list': {'1王': "https://cdn.discordapp.com/attachments/680402200077271106/702486233976274954/a20f65fafc6ab134dee66e9e03b2e07e.png",
                                        '2王': "https://cdn.discordapp.com/attachments/680402200077271106/702486290012307517/75edbc7700db07e068ffbbe1e14fdf71.png",
                                        '3王': "https://cdn.discordapp.com/attachments/680402200077271106/702486362065993728/ee8ccd72f075340d5105c38903681e7b.png",
                                        '4王': "https://cdn.discordapp.com/attachments/680402200077271106/702486425844580362/gateway-3-1.png",
                                        '5王': "https://cdn.discordapp.com/attachments/680402200077271106/702486472317730816/gateway-4-1.png",
                                        '補償清單': "https://cdn.discordapp.com/attachments/680402200077271106/681015805110124554/616147400792342538.png"},
                        'unit_list': {'1王': "W",
                                        '2王': "W",
                                        '3王': "W",
                                        '4王': "W",
                                        '5王': "W",
                                        '補償清單': "S"},
                        'embed_color_list': {'可報_無補': 11199402,
                                            '可報_有補': 16768094,
                                            '不可報': 14913445,
                                            '補償清單': 16777215},


                        'number_emoji': ['0️⃣', '1️⃣', '2️⃣', '3️⃣',
                                        '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '⬅️', '▶️'],

                        'sign_up_emoji': '📄',
                        'cancel_emoji': '🔄',
                        'overflow_emoji': '🔂',
                        'overflow_cancel_emoji': '🆖'
                        } """
""" --------------- Getting Data --------------- """


def admin_check(user_id, bot, self=False):
    if user_id in get_role_members(bot):
        return True
    elif self:
        if f'<@!{user_id}>' in self.admin_check():
            return True
    return False


def get_role_members(bot):
    # 573893554577866777 窩們一起學牛叫：O
    # <@&750720404213203079> @美美管理員
    #
    # 727170387091259393 功德無量
    # 734391146910056478 @TEST
    server = bot.get_guild(727170387091259393)
    role = server.get_role(734391146910056478)
    member_ids = [member.id for member in role.members]
    return member_ids


class list_msg_empty:
    id = 0


def tea_fig_KingIndexToKey(King_List, msg):
    """ TODO:轉換數字->(1~5)王, 無法轉換則回傳原值 """
    try:
        msg = int(msg)
        if(len(King_List) >= int(msg)):
            tmp = list(King_List.keys())
            msg = tmp[msg-1]
    except:
        msg = msg
    return msg


def now_save():
    f = open("./data/now_data.json", "w")
    f.write(f'{now}')
    f.close()


def data_save():
    f = open("./data/data.json", "w")
    f.write(f'{All_OutKnife_Data}')
    f.close()


def admin_save():
    f = open("./data/setting.json", "w")
    f.write(json.dumps(setting_data))
    f.close()


""" def team_fight_setting_save():
    f = open("./data/team_fight_setting.json", "w")
    f.write(f'{team_fight_setting}')
    f.close() """
