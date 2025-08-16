# cogs/basic.py
from twitchio.ext import commands

@commands.command(name="hello")
async def hello(ctx: commands.Context):
    await ctx.send(f"Hello, {ctx.author.name}!")

@commands.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Pong 🏓")

commands_list = [hello, ping]
