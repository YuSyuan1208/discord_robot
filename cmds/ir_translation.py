
import discord
from discord.ext import commands
import random
import json
import array
import sys
from core.classes import Cog_Extension
from model.func import *
import logging
logger = logging.getLogger(__name__)

# 翻譯評到 791162713941475348

class ir_translation(Cog_Extension):

    _name = 'ir_translation'
    _file_data = {}
    _data = {}
    _set_default = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await super().on_ready()

    def _conver_str(self, str):
        if str in self._set_default.keys():
            logger.debug(self._name + f' _conver_str get.(str={str})')
            return self._set_default[str]
        else:
            return str
    
    def _replace_str(self, str):
        for i in self._set_default.keys():
            logger.debug(self._name + f' _replace_str get.(str={i})')
            str = str.replace(i, self._set_default[i])
        return str
        
    @commands.command()
    async def i(self,ctx,msg):
        await ctx.send(self._replace_str(msg))


def setup(bot):
    obj = ir_translation(bot)
    bot.add_cog(obj)
    logging.info(obj._name + ' being loading!')