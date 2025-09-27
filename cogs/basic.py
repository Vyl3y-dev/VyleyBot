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

@commands.command(name="8ball")
async def eight_ball(ctx: commands.commanads.Context, *, question: str = None):
    if question is None:
        await ctx.send(f"@{ctx.author.name}, you need to ask a question! Usage: !8ball <question>")
        return

    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
        "Shiiiet idk mane I'm high asf rn ask me later."
    ]
    
    answer = random.choice(responses)
    await ctx.send(f"🎱 Question: '{question}'\n\n🎱 Magic 8-Ball says: {answer}")

commands_list = [hello, ping, lurk, hug, eight_ball]

