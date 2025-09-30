import os
import json
import random
from typing import List, Dict
from twitchio.ext import commands

DATA_PATH = "data/quotes.json"

def load_quotes() -> List[Dict]:
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_quotes(quotes: List[Dict]):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True) # Ensure directory and file exists.
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)

class Quotes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_mod_or_broadcaster(self, ctx: commands.Context) -> bool: # Let's check whether the user's a mod or Vyley <3
        return bool(getattr(ctx.author, "is_mod", False) or getattr(ctx.author, "is_broadcaster", False))

    @commands.command(name="addquote")
    async def add_quote(self, ctx: commands.Context, *, quote_text: str = None):
        if not self.is_mod_or_broadcaster(ctx):
            return # Silently ignore if not a mod

        if not quote_text:
            return await ctx.send(f"@{ctx.author.name}, pls gib text to quote.")

        quotes = load_quotes()
        
        new_quote = {
            "id": len(quotes) + 1,
            "text": quote_text,
            "added_by": ctx.author.name
        }
        
        quotes.append(new_quote)
        save_quotes(quotes)
        
        await ctx.send(f"Quote #{new_quote['id']} added.")

    @commands.command(name="quote") # Let's pull a random quote from the JSON file.
    async def get_quote(self, ctx: commands.Context):
        quotes = load_quotes()
        
        if not quotes:
            return await ctx.send("There's no quotes in the file. Weird. Ask Vyley to check.")
            
        random_quote = random.choice(quotes)
        
        await ctx.send(f"{random_quote['text']}")

def prepare(bot: commands.Bot):
    # Since we're adding a new cog that will be loaded with the bot (Because we can hotload cogs depending on what we need including mod ones, we can use this to add the cog to the bot.)
    bot.add_cog(Quotes(bot))