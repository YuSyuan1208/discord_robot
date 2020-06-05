import json
import ast

with open('./data/setting.txt', 'r', encoding='utf8') as jfile:
    setting_data = json.load(jfile)
with open('./data/reply_cmds.txt', 'r', encoding='utf8') as jfile:
    reply_data = json.load(jfile)

print("Server Start")
""" template = {'1王': {'資訊': {"header":"","footer":"","hp":600}, '報名列表': []}, 
'2王': {'資訊': {"header":"","footer":"","hp":800}, '報名列表': []}, 
'3王': {'資訊': {"header":"","footer":"","hp":1000}, '報名列表': []}, 
'4王': {'資訊': {"header":"","footer":"","hp":1200}, '報名列表': []}, 
'5王': {'資訊': {"header":"","footer":"","hp":1500}, '報名列表': []}} """



''' OutKnife_Data = {}
OutKnife_Data[0] = {'1王': {'資訊': {"header": "", "footer": "", "hp": 600}, '報名列表': []},
                    '2王': {'資訊': {"header": "", "footer": "", "hp": 800}, '報名列表': []},
                    '3王': {'資訊': {"header": "", "footer": "", "hp": 1000}, '報名列表': []},
                    '4王': {'資訊': {"header": "", "footer": "", "hp": 1200}, '報名列表': []},
                    '5王': {'資訊': {"header": "", "footer": "", "hp": 1500}, '報名列表': []}}

overflow = {'資訊': {"header": "", "footer": "", "hp": 90}, '報名列表': []}

OutKnife_Data[0]['補償清單'] = overflow '''

""" --------------- Initial Parameter --------------- """
All_OutKnife_Data = {}
now = {'周': 1, '王': 1, 'limit_max_week':10}
list_msg_tmp = []  # [week, king, msg]
now_msg = {}
number_insert_msg = {}  # [msg.id] = [user_id, week, king, msg]
robot_id = setting_data['robot_id']
meme_channel = setting_data['meme_channel']
tea_fig_channel = setting_data['tea_fig_channel']
run_out_before_look = setting_data['run_out_before_look']
backup_channel_id = setting_data['backup_channel_id']
only_meme_speak_channel = setting_data['only_meme_speak_channel']

auto_refresh_max = 6*1
team_fight_function_enable = True
""" --------------- Initial Parameter --------------- """

with open('./data/data.txt', 'r') as content_file:
    All_OutKnife_save_data = content_file.read()
All_OutKnife_Data = ast.literal_eval(All_OutKnife_save_data) 
overflow = All_OutKnife_Data[1]["補償清單"]

with open('./data/now.txt', 'r') as content_file:
    now_save_data = content_file.read()
now = ast.literal_eval(now_save_data)

with open('./data/list_msg_tmp.txt', 'r') as content_file:
    list_msg_tmp_id_save_data = content_file.read()
list_msg_tmp_id  = ast.literal_eval(list_msg_tmp_id_save_data)

with open('./data/admin.txt', 'r') as content_file:
    admin_save_data = content_file.read()
setting_data["admin"] = ast.literal_eval(admin_save_data)

for i in range(1, len(All_OutKnife_Data)):
    ''' All_OutKnife_Data[i] = {'1王': {'資訊': {"header": "", "footer": "", "hp": 600}, '報名列表': []},
                            '2王': {'資訊': {"header": "", "footer": "", "hp": 800}, '報名列表': []},
                            '3王': {'資訊': {"header": "", "footer": "", "hp": 1000}, '報名列表': []},
                            '4王': {'資訊': {"header": "", "footer": "", "hp": 1200}, '報名列表': []},
                            '5王': {'資訊': {"header": "", "footer": "", "hp": 1500}, '報名列表': []}} 
    overflow = {'資訊': {"header": "", "footer": "", "hp": 90}, '報名列表': []}'''
    All_OutKnife_Data[i]['補償清單'] = overflow


def id_check(user_id):
    if user_id in setting_data["admin"]:
        return True
    return False

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
    f = open("./data/now.txt", "w")
    f.write(f'{now}')
    f.close() 

def data_save():
    f = open("./data/data.txt", "w")
    f.write(f'{All_OutKnife_Data}')
    f.close()