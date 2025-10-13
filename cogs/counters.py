import os
import json
from typing import List, Dict
from twitchio.ext import commands

DATA_PATH = "data/counters.json"

def load_counters() -> List[Dict]:
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
def save_counters(counters: List[Dict]):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf=8") as f:
        json.dump(counters, f, indent=2, ensure_ascii=False)

class Counters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="fifty")
    async def plusFifty(self, ctx: commands.Context, countedFifty: int = 0):
        fiftyCounter = load_counters()
        countedFifty += 1
        add_plusFifty = {
            "id": len(fiftyCounter) + 1,
            "plusFifty": countedFifty,
        }

        fiftyCounter.append(add_plusFifty)
        save_counters(fiftyCounter)
        
        await ctx.send(f"Vy has claimed @{fiftyCounter} +50's since 10/13/25")
    

def prepare(bot: commands.Bot):
    bot.add_cog(Counters(bot))