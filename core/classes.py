import discord
from discord.ext import commands
from model.func import *

class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.sign_up = 0

