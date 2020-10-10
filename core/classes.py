import discord
from discord.ext import commands
from model.func import *
import logging
import os
logger = logging.getLogger(__name__)


class Cog_Extension(commands.Cog):

    _name = None
    _file_data = {}
    _data = {}

    def __init__(self, bot):
        self.bot = bot
        if self._name:
            logger.info(self._name + ' init')
            self.file('r')
        else:
            logger.error('_name not setting.')
            raise NameError('model _name not setting.')

    def file(self, type):
        if type == 'r':
            if os.path.isfile('./data/'+self._name+'.json'):
                logger.info(self._name + ' file getting.')
                with open('./data/'+self._name+'.json', 'r', encoding='utf8') as jfile:
                    self._file_data = json.load(jfile)
                return True
            else:
                logger.warning(self._name + ' file not find.')
                return False
        elif type == 'w':
            logger.info(self._name + ' file saving.')
            f = open('./data/'+self._name+'.json', 'w')
            f.write(json.dumps(self._file_data))
            f.close()

    async def _get_message_data(self):
        if self._file_data:
            channel_id = self._file_data['channel_id']  # 750943234691432510
            msg_id = self._file_data['msg_id']  # 750946905751814224
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.warning(self._name + f' channel not find.(channel_id={channel_id})')
                return False
            msg = await channel.fetch_message(msg_id)
            logger.debug(self._name + f' fetch_message .(msg.content={msg.content})')
            if not msg:
                logger.warning(self._name + f' message not find.(msg_id={msg_id})')
                return False
            content = msg.content

            self._data = ast.literal_eval(content)
            logger.info(self._name + ' message getting.')
            return True
        else:
            logger.warning(self._name + ' no data.')
            return False
