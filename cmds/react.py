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
""" try:
            
        except:
            await ctx.send(" ```arm\ncommand_error\n``` ex. \*王列表 all ,\*王列表 ?王") """




import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
import array
from model.func import *
import logging
import os
import ast

class React(Cog_Extension):

    # setting
    """ ch_id: 750943234691432510 
    msg_id: 752519979173150771 
    aut_id: 312939009879834624 """

    """ 
    [role]
    @Test   -   <@&734391146910056478> 
    [member]
    @廉價勞工   -   <@!312939009879834624>
    [guild]
    功德無量    -   727170387091259393
    """

    """ @commands.command()
    async def start(self, ctx):
        await ctx. """
    
    _name = 'react'
    _file_data = {}
    _data = {}
    
    def __init__(self, bot):
        super().__init__(bot)
        if self._name:
            logging.debug(self._name + ' init')
            self.file_get()
        else:
            logging.error('_name not setting.')

    def file_get(self):
        if os.path.isfile('./data/'+self._name+'.json'):
            with open('./data/'+self._name+'.json', 'r', encoding='utf8') as jfile:
                self._file_data = json.load(jfile)
            logging.debug(self._name + ' file getting.')
            return True
        else:
            logging.warning(self._name + ' file not find.')
            return False

    def file_save(self):
        f = open('./data/'+self._name+'.json', 'w')
        f.write(json.dumps(self._file_data))
        f.close()

    @commands.command()
    async def _check(self, ctx):
        if self._file_data:
            logging.debug(self._name + ' file already get.')
        else:
            channel_id = ctx.channel.id
            msg = await ctx.send(self._data)
            msg_id = msg.id
            self._file_data.update({'channel_id':channel_id,'msg_id':msg_id})
            self.file_save()
            logging.debug(self._name + ' file created.')


    @commands.Cog.listener()
    async def on_ready(self):
        pass
        """ channel_id = 750943234691432510
        msg_id = 750946905751814224 
        channel = self.bot.get_channel(channel_id)
        msg = await channel.fetch_message(msg_id)
        content = msg.content

        data = react_data
        tmp = content.split('\n')
        for i in tmp:
            print(i)
            tmp2 = i.split(':')
            data[tmp2[0]] = tmp2[1]
        print('react_data 獲取成功') """
        if await self.get_react_data():
            self.add_command()

    async def get_react_data(self):
        if self._file_data:
            channel_id = self._file_data['channel_id'] #750943234691432510
            msg_id = self._file_data['msg_id'] #750946905751814224 
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logging.warning(self._name + f' channel not find.({channel_id})')
            msg = await channel.fetch_message(msg_id)
            if not msg:
                logging.warning(self._name + f' message not find.({msg_id})')
            content = msg.content

            self._data = ast.literal_eval(content)
            logging.debug(self._name + ' message getting.')
            return True
        else:
            logging.warning(self._name + ' no data.')
            return False
    
    def add_command(self):
        if self._data:
            for name in self._data:
                obj = cms_class()
                obj.msg = self._data[name]
                self.bot.add_command(commands.Command(obj.add_cmd,name=name))
            logging.debug(self._name + ' cmds complete.')
            return True
        else:
            logging.warning(self._name + ' cmds no data.')
            return False

    @commands.command()
    async def at(self, ctx, *msg):
        content = ' '.join(msg[0:])
        print(content)
        self._data.update(ast.literal_eval(content))
        self.add_command()
        await self.msg_change()

    @commands.command()
    async def msg_change(self):
        if self._file_data:
            channel_id = self._file_data['channel_id'] #750943234691432510
            msg_id = self._file_data['msg_id'] #750946905751814224 
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logging.warning(self._name + f' channel not find.({channel_id})')
            msg = await channel.fetch_message(msg_id)
            if not msg:
                logging.warning(self._name + f' message not find.({msg_id})')
            await msg.edit(content = self._data)
        


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user_id = payload.user_id
        channel_id = payload.channel_id
        message_id = payload.message_id
        channel = self.bot.get_channel(channel_id)
        print('ch_id:',channel_id,'user_id:',user_id,'pay:',payload )

        channel_id = 750936316979707974
        msg_id = 750945386851467325 
        channel = self.bot.get_channel(channel_id)
        msg = await channel.fetch_message(msg_id)
        if payload.emoji.name == msg.content: # 相等
            print(True)
        else:
            print(payload.emoji.name,msg.content)

    @commands.command(description="")
    async def test(self, ctx):
        pass


class cms_class:
    msg = []
    author_id = 0
    channel_id = 0
    async def add_cmd(self,ctx):
        await ctx.send(random.choice(self.msg).format(ctx=ctx))

# @commands.command()
# async def aaa(self,ctx):
#     await ctx.send('Hello {0.display_name}.'.format(ctx.author))

def setup(bot):
    obj = React(bot)
    #obj.add_command(commands.Command("aaa", aaa))
    bot.add_cog(obj)
    #bot.add_command(aaa)

# @commands.command(description="EX. *hello", brief="EX. *hello")
# async def hello(self, ctx):
#     await ctx.send(reply_data["hello"].format(ctx=ctx))

# @commands.command(description="EX. *蹦蹦跳", brief="EX. *蹦蹦跳")
# async def 蹦蹦跳(self, ctx):
#     await ctx.send(reply_data["蹦蹦跳"].format(ctx=ctx))

# @commands.command(description="EX. *運勢", brief="EX. *運勢")
# async def 運勢(self, ctx):
#     await ctx.send(random.choice(reply_data["運勢"]).format(ctx=ctx))

# @commands.command(description="EX. *胖次", brief="EX. *胖次")
# async def 胖次(self, ctx):
#     await ctx.send(random.choice(reply_data["胖次"]).format(ctx=ctx))

# @commands.command(description="EX. *棒棒糖", brief="EX. *棒棒糖")
# async def 棒棒糖(self, ctx):
#     await ctx.send(reply_data["棒棒糖"].format(ctx=ctx))

# @commands.command(description="EX. *鏡華噴水水", brief="EX. *鏡華噴水水")
# async def 鏡華噴水水(self, ctx):
#     await ctx.send(reply_data["鏡華噴水水"].format(ctx=ctx))

# @commands.command(description="EX. *鏡華", brief="EX. *鏡華")
# async def 鏡華(self, ctx):
#     await ctx.send(reply_data["鏡華"].format(ctx=ctx))

# @commands.command(description="EX. *褉", brief="EX. *褉")
# async def 褉(self, ctx):
#     await ctx.send(reply_data["褉"].format(ctx=ctx))

# @commands.command(description="EX. *幹起來", brief="EX. *幹起來")
# async def 幹起來(self, ctx):
#     await ctx.send(f'{ctx.author.mention}幹起來幹起來<:kokoro:606693439647776777>')

# @commands.command(description="EX. *無所屬 <tag>", brief="EX. *無所屬 <tag>")
# async def 無所屬(self, ctx, msg):
#     await ctx.send(f'{msg}你已成為無所屬大隊長,掰掰<:kokoro:606693439647776777>')

# @commands.command(description="EX. *魚", brief="EX. *魚")
# async def 魚(self, ctx):
#     await ctx.send(f'https://media.discordapp.net/attachments/573893555052085249/677104072804794368/received_469379323565972.gif')

# @commands.command(description="EX. *徵人", brief="EX. *徵人")
# async def 徵人(self, ctx):
#     await ctx.send(f'徵求discord robot程式作業員, 日薪: <@!336858626981494785>的鼓勵和拍拍<:kokoro:606693439647776777>')

# @commands.command(description="EX. *我要", brief="EX. *我要")
# async def 我要(self, ctx):
#     await ctx.send(f'{ctx.author.mention}我就交給你了<:MeMe:616147400792342538>')

# @commands.command(description="EX. *鬧憋扭", brief="EX. *鬧憋扭")
# async def 鬧憋扭(self, ctx):
#     await ctx.send(f'https://media.discordapp.net/attachments/573893555052085249/663074402287747082/ezgif-4-4d02dd86d8e0.gif')

# @commands.command(description="EX. *並沒有", brief="EX. *並沒有")
# async def 並沒有(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/573893555052085249/681109507027501056/d3420288.png')

# @commands.command(description="EX. *不要瞎掰好嗎", brief="EX. *不要瞎掰好嗎")
# async def 不要瞎掰好嗎(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/573893555052085249/681109867473403953/d3420289.png')

# @commands.command(description="EX. *接頭", brief="EX. *接頭")
# async def 接頭(self, ctx):
#     tmp = ['https://media.discordapp.net/attachments/483550384133111808/677509375723831311/kyaruuuuu.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/682218851001434160/96cbe038ca76cf0cf2c0f682852900c7.png',
#            'https://cdn.discordapp.com/attachments/573893555052085249/682219043435970590/ab19e3d7b4944e05a431f8880eb85c18.png']
#     await ctx.send(random.choice(tmp))

# @commands.command(description="EX. *介紹 <tag>", brief="EX. *介紹 <tag>")
# async def 介紹(self, ctx, msg):
#     await ctx.send(f'{msg}是一個熱愛工作不求~~薪水~~回報的~~工具人~~好勞工')

# @commands.command(description="EX. *我全都要", brief="EX. *我全都要")
# async def 我全都要(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/573893555052085249/681111278026227758/cmjxSxC.gif')

# @commands.command(description="EX. *過勞", brief="EX. *過勞")
# async def 過勞(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/573893555052085249/681112177859625019/image0.jpg')

# @commands.command(description="EX. *發瘋", brief="EX. *發瘋")
# async def 發瘋(self, ctx):
#     tmp = ['https://cdn.discordapp.com/attachments/573893555052085249/681117980230287420/v2-0f1a666e5bb6db7f57f7e760756ed9ed_hd.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681118057803939866/tenor_19.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681118142789058589/tenor_7-1.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681118244220043287/SmWnZXg.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681117998626373659/shake.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681118739395248335/8f28dd0a6506cd028eff3d107a526b09.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681119137497743380/aaa.gif',
#            'https://tenor.com/view/yeeeeaaah-yes-celebrating-happy-tube-man-gif-16295308',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681119469866975248/1536270767-3.gif',
#            'https://tenor.com/view/rabbids-invasion-laugh-gif-13933309',
#            'https://tenor.com/view/yall-mind-if-ipraise-the-lord-praise-dance-praise-dance-praise-the-lord-gif-11921222',
#            'https://tenor.com/view/seal-smile-happy-gif-16358463',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681119713220493314/974cd01a70dc313dc3eedbbe7420179355bf7aa0_00.gif',
#            'https://tenor.com/view/bird-parrot-papagallo-amitico-party-gif-8906272',
#            'https://tenor.com/view/iwill-be-back-shade-brb-give-me-aminute-hold-on-gif-16340332',
#            'https://cdn.discordapp.com/emojis/621300822692855808.gif?v=1',
#            'https://tenor.com/view/stoned-baked-high-nicholas-cage-gif-9879658',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681120206164459731/71167966_2522061951172698_6850133586243223552_n.jpg',
#            'https://tenor.com/view/excited-hockey-kid-gif-10474493',
#            'https://tenor.com/view/bird-parrot-papagallo-amitico-party-gif-8906272',
#            'https://tenor.com/view/crazy-alert-crazy-alert-alerta-alerta-loca-gif-15115104']
#     await ctx.send(random.choice(tmp))

# @commands.command(description="EX. *這個", brief="EX. *這個")
# async def 這個(self, ctx):
#     tmp = ['https://cdn.discordapp.com/attachments/573893555052085249/681457731764617221/ef07e73f031d584c.gif',
#            'https://cdn.discordapp.com/attachments/573893555052085249/681457126954369047/3.gif']
#     await ctx.send(random.choice(tmp))

# @commands.command(description="EX. *割傷", brief="EX. *割傷")
# async def 割傷(self, ctx):
#     await ctx.send(f'血小板跑出來了https://cdn.discordapp.com/attachments/573893555052085249/681453485627408406/tenor2.gif')

# @commands.command(description="EX. *steal", brief="EX. *steal")
# async def steal(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/573893555052085249/681463568977231872/DirtyPertinentAyeaye-max-1mb.gif')

# @commands.command(description="EX. *c8763, *星爆氣流斬", name='星爆氣流斬', aliases=['c8763'], brief="EX. *c8763, *星爆氣流斬")
# async def 星爆氣流斬(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/680402200077271106/681874303922339852/UfXTSPn.gif')

# @commands.command(description="EX. *爆肝", brief="EX. *爆肝")
# async def 爆肝(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/680402200077271106/681875143181598730/UfXTSPn.gif')

# @commands.command(description="EX. *崩潰", brief="EX. *崩潰")
# async def 崩潰(self, ctx):
#     await ctx.send(f'https://media.discordapp.net/attachments/438316027546173450/633944639036194843/20190506_212437.gif')

# @commands.command(description="EX. *脫胖次", brief="EX. *脫胖次")
# async def 脫胖次(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/emojis/594988644612177930.gif?v=1')

# @commands.command(description="EX. *藍色, *blue, *智障", name='藍色', aliases=['blue', '智障'], brief="EX. *藍色, *blue, *智障")
# async def 藍色(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/680402200077271106/682211376579739879/test.gif')

# @commands.command(description="EX. *時間暫停, *TheWorld", name='時間暫停', aliases=['TheWorld'], brief="EX. *時間暫停, *TheWorld")
# async def 時間暫停(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/680402200077271106/682213464994873371/f484ae35c6dc54e5.gif')

# @commands.command(description="EX. *骨灰盒", brief="EX. *骨灰盒")
# async def 骨灰盒(self, ctx):
#     await ctx.send(f'https://media.discordapp.net/attachments/393106451599458308/681393904020619365/1_20190718_16c048328e9166884.gif')

# @commands.command(description="EX. *自爆", brief="EX. *自爆")
# async def 自爆(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/680402200077271106/682213923637952587/FUC3Srf.gif')

# @commands.command(description="EX. *歐拉歐拉", brief="EX. *歐拉歐拉")
# async def 歐拉歐拉(self, ctx):
#     await ctx.send(f'https://cdn.discordapp.com/attachments/680402200077271106/682214670614134803/fcf7fef28febff59a657149ab4c552ad.gif')

# @commands.command(description="EX. *黃金體驗", brief="EX. *黃金體驗")
# async def 黃金體驗(self, ctx):
#     tmp = ['https://imgur.com/milTjRF', 'https://imgur.com/cKGTcC5', 'https://imgur.com/pDP10ns'
#            'https://cdn.discordapp.com/attachments/493695553906016258/680787799338647555/unknown.png']
#     await ctx.send(random.choice(tmp))

# @commands.command(description="EX. *婆", name='婆', aliases=['<:wife:611740459378933761>'], brief="EX. *婆")
# async def 婆(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/573893555052085249/682220377954320384/nd3yg.gif')

# @commands.command(description="EX. *我就爛", brief="EX. *我就爛")
# async def 我就爛(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682514369136820238/c0125aa64ab7a12a43ae28ffc892f886.jpg')

# @commands.command(description="EX. *救", brief="EX. *救")
# async def 救(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682514445137739842/image0.jpg')

# @commands.command(description="EX. *洗臉", brief="EX. *洗臉")
# async def 洗臉(self, ctx):
#     await ctx.send('https://images-ext-1.discordapp.net/external/ft9vavBVGc8q96-x-THvv0zodySzHoJPoXNSUsKTdYU/https/media.discordapp.net/attachments/573893555052085249/682548906969923654/61YUEMnsOAH02mAsbiV0ZY.gif')

# @commands.command(description="EX. *假的", brief="EX. *假的")
# async def 假的(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682597477311840259/test.gif')

# @commands.command(description="EX. *沒救了", brief="EX. *沒救了")
# async def 沒救了(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682599486505222149/test.gif')

# @commands.command(description="EX. *發薪水", brief="EX. *發薪水")
# async def 發薪水(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682854042912948266/tenor.gif')

# @commands.command(description="EX. *我好興奮", brief="EX. *我好興奮")
# async def 我好興奮(self, ctx):
#     tmp = ['https://tenor.com/view/excited-adorable-agt-agtgifs-americas-got-talent-gif-10812006',
#            'https://cdn.discordapp.com/attachments/680402200077271106/682853260930842624/tenor.gif']
#     await ctx.send(random.choice(tmp))

# @commands.command(description="EX. *QQ軟糖", brief="EX. *QQ軟糖")
# async def QQ軟糖(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/573893555052085249/682881172677853193/87072862_3327035467330914_1445000240175251456_n.jpg')

# @commands.command(description="EX. *打臉", brief="EX. *打臉")
# async def 打臉(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/483550384133111808/682846397875355698/tenor-19.gif')

# @commands.command(description="EX. *舔起來", brief="EX. *舔起來")
# async def 舔起來(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682914940247343123/484948976723034123.gif')

# @commands.command(description="EX. *抓到", brief="EX. *抓到")
# async def 抓到(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682914070101360645/80896014_2611137925674622_6621517274555613184_n.jpg')

# @commands.command(description="EX. *以豹制豹", brief="EX. *以豹制豹")
# async def 以豹制豹(self, ctx):
#     await ctx.send('https://tenor.com/view/%e4%bb%a5%e8%b1%b9%e5%88%b6%e8%b1%b9-fight-sea-lion-animals-gif-14162295')

# @commands.command(description="EX. *FBI", brief="EX. *FBI")
# async def FBI(self, ctx):
#     tmp = ['https://media.discordapp.net/attachments/634648615758856192/669588792813944833/image0.gif',
#            'https://cdn.discordapp.com/attachments/389480470678863883/672756878748549150/image0.gif']
#     await ctx.send(random.choice(tmp))

# @commands.command(description="EX. *蹭大腿", brief="EX. *蹭大腿")
# async def 蹭大腿(self, ctx):
#     tmp = ['https://cdn.discordapp.com/attachments/573893555052085249/682957995843387415/gIzQ2.gif',
#            'https://media.discordapp.net/attachments/548494727155023874/639823631026880573/555.gif']
#     await ctx.send(random.choice(tmp))

# @commands.command(description="EX. *射爆", brief="EX. *射爆")
# async def 射爆(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/633286205362012170/648023140525670410/tenor.gif')

# @commands.command(description="EX. *奶子", brief="EX. *奶子")
# async def 奶子(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/682954704581558362/DCNuUmz.png')

# @commands.command(description="EX. *猜拳 <剪刀,石頭,布>", brief="EX. *猜拳 <剪刀,石頭,布>")
# async def 猜拳(self, ctx, msg):
#     author_id = ctx.author.id
#     tmp = ['https://media.discordapp.net/attachments/634648615758856192/666327608958517291/image0.gif',
#            'https://media.discordapp.net/attachments/634648615758856192/666327610371866625/image1.gif',
#            'https://media.discordapp.net/attachments/634648615758856192/666327611047280650/image2.gif']
#     r = random.randint(0, 2)
#     send_msg = ''
#     if((r == 0 and msg == "剪刀") or (r == 1 and msg == "石頭") or (r == 2 and msg == "布")):
#         send_msg = f'<@!{author_id}>大哥哥是平手呢(๑•᎑•๑) {tmp[r]}'
#     elif((r == 0 and msg == "石頭") or (r == 1 and msg == "布") or (r == 2 and msg == "剪刀")):
#         send_msg = f'<@!{author_id}>大哥哥是你贏了(๑•́︿•̀๑) {tmp[r]}'
#     elif((r == 0 and msg == "布") or (r == 1 and msg == "剪刀") or (r == 2 and msg == "石頭")):
#         send_msg = f'<@!{author_id}>大哥哥是我贏了٩(ˊᗜˋ*)و {tmp[r]}'
#     await ctx.send(send_msg)

# @commands.command(description="EX. *拜託", brief="EX. *拜託")
# async def 拜託(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/573893555052085249/682960634518044690/Gochiusa_35.gif')

# @commands.command(description="EX. *計畫通", brief="EX. *計畫通")
# async def 計畫通(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/573893555052085249/683961258541842467/1qp2000027031n60218p.png?width=573&height=573')

# @commands.command(description="EX. *畫畫", brief="EX. *畫畫")
# async def 畫畫(self, ctx):
#     await ctx.send('美美畫好了，你猜猜這是什麼٩(ˊᗜˋ*)وhttps://cdn.discordapp.com/attachments/573893555052085249/684012574726946826/unknown.png')

# @commands.command(description="EX. *吃餅", brief="EX. *吃餅")
# async def 吃餅(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/680402200077271106/683661994770825302/1526192646205o10on55493.gif')

# @commands.command(description="EX. *白嫖", brief="EX. *白嫖")
# async def 白嫖(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/680402200077271106/683662002014650368/152619250550773887r9rr8.gif')

# @commands.command(description="EX. *月黑風高", brief="EX. *月黑風高")
# async def 月黑風高(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/680402200077271106/683662004061339658/1526192577563376q31r858.gif')

# @commands.command(description="EX. *看三小", brief="EX. *看三小")
# async def 看三小(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/573893555052085249/684034051270901760/1583156824730.gif')

# @commands.command(description="EX. *鏡花水月", brief="EX. *鏡花水月")
# async def 鏡花水月(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/483550384133111808/684425578329538578/o0DjHK98nu7T.png?width=693&height=574')

# @commands.command(description="EX. *我很好奇", brief="EX. *我很好奇")
# async def 我很好奇(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/680402200077271106/687163216278585374/2.gif')

# @commands.command(description="EX. *但是我拒絕", brief="EX. *但是我拒絕")
# async def 但是我拒絕(self, ctx):
#     await ctx.send('https://cdn.discordapp.com/attachments/573893555052085249/699220976650551427/134858caf54fa9b0.gif')

# @commands.command(description="EX. *看著我的眼睛", brief="EX. *看著我的眼睛")
# async def 看著我的眼睛(self, ctx):
#     await ctx.send('https://media.discordapp.net/attachments/420229163606212618/689656619646451732/image0.gif')

# @commands.command(description="EX. *安妮沒大", brief="EX. *安妮沒大")
# async def 安妮沒大(self, ctx):
#     await ctx.send('https://www.twitch.tv/ushikun_6927/clip/MistyFitOxBigBrother')
# @commands.command(description="EX. *臭甲", brief="EX. *臭甲")
# async def 臭甲(self, ctx):
#     await ctx.send('https://www.twitch.tv/ushikun_6927/clip/SparklyJazzyShinglePlanking')
