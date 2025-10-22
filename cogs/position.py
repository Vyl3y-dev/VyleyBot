from twitchio.ext import commands

class Position(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Changed to store in memory instead of file, as we want it to reset every time bot is started.
        self.positions = {}

    @commands.command(name="first")
    async def first(self, ctx: commands.Context):
        held_position = self.positions.get("first")
        
        if not held_position:
            self.positions["first"] = ctx.author.name
            await ctx.send(f"{ctx.author.name} is first! <3")
            else:
                await ctx.send(f"{held_position} was already first!")

    @commands.command(name="second")
    async def second(self, ctx: commands.Context):
        held_position = self.positions.get("second")

        if not held_position:
            self.positions["second"] = ctx.author.name
            await ctx.send(f"{ctx.author.name} is second! <3")
        else:
            await ctx.send(f"{held_position} was already second!")
    
def prepare(bot: commands.Bot):
    bot.add_cog(Position(bot))