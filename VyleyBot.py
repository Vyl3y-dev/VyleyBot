from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token='oauth:your_token_here', prefix='!',
                         initial_channels=['your_channel_name'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        print(f'{message.author.name}: {message.content}')
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name}!')

bot = Bot()
bot.run()