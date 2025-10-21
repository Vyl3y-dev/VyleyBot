import os
import json
from typing import Dict
from twitchio.ext import commands

DATA_PATH = "data/position.json"

def load_position() -> Dict:
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    
def save_position(position: Dict):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(position, f, indent=2, ensure_ascii=False)

class Position(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="first")
    async def first(self, ctx: commands.Context):
        positionHolder = load_position()
        heldPosition = positionHolder.get("calledFirst", "")
        
        if heldPosition == "":
            positionHolder["calledFirst"] = ctx.author.name
            save_position(positionHolder)
            await ctx.send(f"{heldPosition} is First!")
        else:
            await ctx.send(f"{heldPosition} was First!")

    @commands.command(name="second")
    async def second(self, ctx: commands.Context):
        positionHolder = load_position()
        heldPosition = positionHolder.get("calledSeccond", "")
        
        if heldPosition == "":
            positionHolder["calledSecond"] = ctx.author.name
            save_position(positionHolder)
            await ctx.send(f"{heldPosition} is Second!")
        else:
            await ctx.send(f"{heldPosition} was Second!")
    
def prepare(bot: commands.Bot):
    bot.add_cog(Position(bot))