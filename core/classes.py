import logging
import os
import sys
import random
import discord
from discord.ext import commands
from model.func import *

logger = logging.getLogger(__name__)


class Cog_Extension(commands.Cog):

    _name = None
    _file_data = {}
    _data = {}

    def __init__(self, bot):
        """  """
        self.bot = bot
        if self._name:
            logger.info(self._name + ' init')
            self.file('r')
        else:
            logger.error('_name not setting.')
            raise NameError('model _name not setting.')

    def file(self, type):
        """ file control """
        if type == 'r':
            if os.path.isfile('./data/'+self._name+'.json'):
                logger.info(self._name + ' file getting.')
                try:
                    with open('./data/'+self._name+'.json', 'r', encoding='utf8') as jfile:
                        self._file_data = json.load(jfile)
                    return True
                except Exception as e:
                    raise ValueError(f'file getting error.(message={sys.exc_info()})')
            else:
                logger.warning(self._name + ' file not find.')
                return False
        elif type == 'w':
            logger.info(self._name + ' file saving.')
            f = open('./data/'+self._name+'.json', 'w')
            f.write(json.dumps(self._file_data))
            f.close()
        raise ValueError(f'type not find.(type={type})')

    def _str_to_list(self, str):
        """ covert message object content to list """
        ast_content = ast.literal_eval(str)
        return ast_content

    async def _get_message_obj(self, channel_id=0, msg_ids=[], history=True, setting={}):
        """ Get message object.

            return message object array (msg_objs)
        """
        limit = setting.get('limit', 100)

        if channel_id:
            # channel_id = self._file_data['channel_id']  # 750943234691432510
            # msg_ids = [self._file_data['msg_id']]  # 750946905751814224
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.warning(self._name + f' channel not find.(channel_id={channel_id})')
                return False

            msg_objs = []
            com_msg_ids = []
            if history:
                logger.info(self._name + ' channel history content getting.')
                async for message in channel.history(limit=int(limit)):
                    if not msg_ids or message.id in msg_ids:
                        msg_objs.append(message)
                        com_msg_ids.append(message.id)
                        logger.debug(self._name + f' message.id: {message.id}')

                com_msg_ids = set(msg_ids) - set(com_msg_ids)
                if com_msg_ids:
                    logger.warning(self._name + f' message not find.(msg_id={com_msg_ids})')
            else:
                logger.info(self._name + ' channel fetch_message content getting.')
                for msg_id in msg_ids:
                    try:
                        message = await channel.fetch_message(msg_id)
                        msg_objs.append(message)
                    except:
                        logger.warning(self._name + f' message not find.(msg_id={msg_id})')

            logger.info(self._name + ' message object get.')
            if not msg_objs:
                logger.warning(self._name + ' no message object data.')
                return False
            else:
                return msg_objs
        else:
            logger.warning(self._name + ' no message object data.')
            return False

    async def _get_message_setting(self):
        """ 依據檔案的channel、message id 取得message object """
        msg_ids = [self._file_data['msg_id']]
        channel_id = self._file_data['channel_id']
        msg_objs = await self._get_message_obj(channel_id=channel_id, msg_ids=msg_ids)
        if msg_objs:
            self._set_default = self._str_to_list(msg_objs[0].content)
            logger.debug(self._name + f' _set_default: {self._set_default}')
            if self._set_default:
                logger.info(self._name + ' _set_default get.')
            else:
                logger.warning(self._name + ' _set_default not get.')
        else:
            logger.warning(self._name + f' _set_default msg_objs not get.')

    def _set_command(self, msg_id, name, setting={}, init_flag=False):
        """ 設定指令 """
        if name:
            cmd_obj = self.bot.get_command(name)
            if cmd_obj:
                logger.debug(self._name + f' ins_com: {name},{setting}')
                obj = cmd_obj.callback.__self__
                if obj.id == msg_id or not init_flag:
                    obj.content = setting['content']
                else:
                    logger.warning(self._name + f' command name repeat.')
            else:
                logger.debug(self._name + f' add_com: {name},{setting}')
                obj = cms_class()
                obj.id = msg_id
                obj.content = setting['content']
                obj.obj_type = self._name
                self.bot.add_command(commands.Command(obj.add_cmd, name=name))
            logger.info(self._name + ' cmds complete.')
            return True
        else:
            logger.warning(self._name + ' name not set.')
            return False

class cms_class:
    id = 0
    content = []
    obj_type = ''

    async def add_cmd(self, ctx, *argv, **knews):
        await ctx.send(random.choice(self.content).format(ctx=ctx, argv=argv, knews=knews))
