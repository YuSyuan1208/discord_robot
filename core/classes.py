import discord
from discord.ext import commands
import logging
import os
import random
from model.func import *

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

    async def _get_message_obj(self, msg_ids=[], history=True, **knews):
        """ Get message object.

        """
        limit = knews.get('limit',100)

        if self._file_data:
            channel_id = self._file_data['channel_id']  # 750943234691432510
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
                com_msg_ids = set(msg_ids) - set(com_msg_ids)
                if com_msg_ids:
                    logger.warning(self._name + f' message not find.(msg_id={com_msg_ids})')
            else:
                logger.info(self._name + ' channel fetch_message content getting.')
                for msg_id in msg_ids:
                    try:
                        message = await channel.fetch_message(msg_id)
                    except:
                        logger.warning(self._name + f' message not find.(msg_id={msg_id})')
                    msg_objs.append(message)

            logger.info(self._name + ' message object get.')
            return msg_objs
        else:
            logger.warning(self._name + ' no data.')
            return False


class cms_class:
    id = 0
    msg = []
    async def add_cmd(self, ctx, *argv):
        await ctx.send(random.choice(self.msg).format(ctx=ctx, input=argv))
