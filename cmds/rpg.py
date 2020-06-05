import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
import array
from model.func import *
import sys

class RPG(Cog_Extension):
    """ @commands.command()
    async def 登記冒險者(self, ctx):
        STR = random.randint(1,20)
        CON = random.randint(1,20)
        INT = random.randint(1,20)
        MEN = random.randint(1,20)
        AGI = random.randint(1,20)
        LUK = random.randint(1,20)
        await ctx.send(STR,CON,INT,MEN,AGI,LUK) """


def setup(bot):
    bot.add_cog(RPG(bot))