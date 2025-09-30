from twitchio.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_first_message(self, message): # twitchio apparently has a built-in event for first-time chatters, let's use it for simplicity :3
        if message.echo or message.author.name == self.bot.nick:
            return # We want to ignore echo messages and messages from the bot itself.

        print(f"First-time chatter detected: {message.author.name}")
        await message.channel.send(f"Embrace chaos, @{message.author.name}, welcome. 👋")

def prepare(bot: commands.Bot):
    bot.add_cog(Welcome(bot))