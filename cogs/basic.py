# cogs/basic.py
from twitchio.ext import commands
import random # < -- Adding this for later, maybe to be used for !8ball or so?

@commands.command(name="hello")
async def hello(ctx: commands.Context):
    await ctx.send(f"Hello, {ctx.author.name}!")

@commands.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Pong 🏓")

@commands.command(name="lurk")
async def lurk(ctx: commands.Context):
    await ctx.send(f"@{ctx.author.name} is lurking in the shadows...")

@commands.command(name="hug") # Just a hug command :3
async def hug(ctx: commands.Context, *, user: str = None):
    hug_emotes = ["theter52DrobenUbu", "theter52ZoeUwU", "theter52LuxUwU", "<3", "theter52SipSip"]
    
    target_user = ""
    if user:
        target_user = user.strip().lstrip('@') # Removes the @ if someone pings the user with it.

    if not target_user:
        message = f"@{ctx.author.name} gets a big, warm hug! {random.choice(hug_emotes)}"
    else:
        message = f"@{ctx.author.name} gives @{target_user} a super cozy hug! {random.choice(hug_emotes)}"
        
    await ctx.send(message)

commands_list = [hello, ping, lurk, hug]
