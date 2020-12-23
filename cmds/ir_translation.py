
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

def setup(bot):
    obj = ir_translation(bot)
    bot.add_cog(obj)
    logging.info(obj._name + ' being loading!')