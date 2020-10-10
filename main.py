# coding=UTF-8
import random
import discord
from discord.ext import commands
import json
import os
from model.func import *
#import keep_alive
import re
import logging
from logging.config import fileConfig
# 读取日志配置文件内容
logging.config.fileConfig('.\\data\\logging_config.ini')


logger_discord = logging.getLogger('discord')

logger = logging.getLogger(__name__)


# logger_root = logging.getLogger(name = 'root')
# discord.client
# logger = logging.getLogger('simple_logger')
# logger.setLevel(logging.DEBUG)

bot = commands.Bot(
    command_prefix=setting_data['BOT_PREFIX'], case_insensitive=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # logger_root.debug('main test.')


@bot.event
async def on_resumed():
    print('embed_color_list')


@bot.command()
async def load(ctx, extension):
    author_id = ctx.author.id
    if(admin_check(author_id) == True):
        if os.path.isfile(f'.\\cmds\\{extension}'):
            bot.load_extension(f'cmds.{extension}.py')
            await ctx.send(f'Loaded {extension}')
        else:
            logger.warning(f'Extension cmds.{extension} could not be loaded.')


@bot.command()
async def unload(ctx, extension):
    author_id = ctx.author.id
    if(admin_check(author_id) == True):
        if os.path.isfile(f'.\\cmds\\{extension}.py'):
            bot.unload_extension(f'cmds.{extension}')
            await ctx.send(f'Unloaded {extension}')
        else:
            logger.warning(f'Extension cmds.{extension} has not been loaded')


@bot.command()
async def reload(ctx, extension):
    author_id = ctx.author.id
    if(admin_check(author_id) == True):
        if os.path.isfile(f'.\\cmds\\{extension}.py'):
            bot.reload_extension(f'cmds.{extension}')
            await ctx.send(f'Reloaded {extension}')
        else:
            logger.warning(f'Extension cmds.{extension} has not been loaded')

# help ending note
""" bot.help_command.get_ending_note """

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        if not team_fight_function_enable:
            if filename == 'team_fight.py':
                continue
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    # keep_alive.keep_alive()
    bot.run(setting_data['TOKEN'])
