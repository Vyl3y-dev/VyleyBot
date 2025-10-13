import os
import json
from typing import Dict
from twitchio.ext import commands

DATA_PATH = "data/counters.json"

def load_counters() -> Dict:
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
    
def save_counters(counters: Dict):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(counters, f, indent=2, ensure_ascii=False)

class Counters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="fifty")
    async def fifty(self, ctx: commands.Context):
        fiftyCounter = load_counters()
        countedFifty = fiftyCounter.get("plusFifty", 0)
        countedFifty += 1
        fiftyCounter["plusFifty"] = countedFifty
        save_counters(fiftyCounter)
        await ctx.send(f"Vy has claimed @{countedFifty} +50's since 10/13/25")
    

def prepare(bot: commands.Bot):
    bot.add_cog(Counters(bot))