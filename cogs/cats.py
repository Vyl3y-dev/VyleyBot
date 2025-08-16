# cogs/cats.py
import os
import json
from typing import List, Dict, Optional
from twitchio.ext import commands

DATA_PATH = "data/cats.json"

def load_cats() -> List[Dict]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cats(cats: List[Dict]):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(cats, f, indent=2, ensure_ascii=False)

def find_cat(cats: List[Dict], name: str) -> Optional[Dict]:
    lname = name.lower()
    for c in cats:
        if c["name"].lower() == lname:
            return c
    return None

class Cats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="cats")
    async def cats(self, ctx: commands.Context):
        """List adoptable cats."""
        cats = load_cats()
        available = [c for c in cats if not c.get("adopted_by")]
        if not cats:
            return await ctx.send("No cats configured yet. (Mods can use !addcat)")
        if not available:
            return await ctx.send("All cats have been adopted! 🐾")
        names = ", ".join(f"{c['name']} ({c['personality']})" for c in available[:10])
        extra = "" if len(available) <= 10 else f" …and {len(available)-10} more"
        await ctx.send(f"Adoptable cats: {names}{extra}. Use !adopt <name> to adopt!")

    @commands.command(name="mycat")
    async def mycat(self, ctx: commands.Context):
        """Show which cat you adopted, if any."""
        user = ctx.author.name.lower()
        cats = load_cats()
        mine = [c for c in cats if c.get("adopted_by", "").lower() == user]
        if not mine:
            return await ctx.send(f"@{ctx.author.name}, you haven’t adopted a cat yet. Use !cats to see who’s available!")
        # If you want multiple per user, this lists all. Otherwise assume first.
        first = mine[0]
        await ctx.send(f"@{ctx.author.name} adopted {first['name']} 🐱 — {first['personality']}")

    @commands.command(name="adopt")
    async def adopt(self, ctx: commands.Context, *, catname: str = None):
        """Adopt a specific cat by name (first-come-first-serve)."""
        if not catname:
            return await ctx.send("Usage: !adopt <catname> (see !cats)")
        cats = load_cats()

        # Prevent multiple adoptions by the same user (optional rule)
        user = ctx.author.name
        if any(c.get("adopted_by", "").lower() == user.lower() for c in cats):
            return await ctx.send(f"@{user}, you already adopted a cat! Use !mycat 🐾")

        cat = find_cat(cats, catname)
        if not cat:
            return await ctx.send(f"No cat named '{catname}' found. Try !cats.")
        if cat.get("adopted_by"):
            return await ctx.send(f"{cat['name']} is already adopted by @{cat['adopted_by']} 😿")

        cat["adopted_by"] = user
        save_cats(cats)
        await ctx.send(f"Congrats @{user}! You adopted {cat['name']} 🎉🐈 {cat['personality']}")

    # ---------- Mod / Admin helpers ----------

    def is_mod_or_broadcaster(self, ctx: commands.Context) -> bool:
        perms = getattr(ctx.author, "is_mod", False) or getattr(ctx.author, "is_broadcaster", False)
        return bool(perms)

    @commands.command(name="addcat")
    async def addcat(self, ctx: commands.Context, name: str = None, *, personality: str = "mysterious"):
        """(Mod) Add a new cat. Usage: !addcat Miso Sleepy keyboard gremlin"""
        if not self.is_mod_or_broadcaster(ctx):
            return
        if not name:
            return await ctx.send("Usage: !addcat <name> <personality...>")

        cats = load_cats()
        if find_cat(cats, name):
            return await ctx.send(f"A cat named '{name}' already exists.")
        cats.append({"name": name, "personality": personality, "sprite": "", "adopted_by": None})
        save_cats(cats)
        await ctx.send(f"Added new cat: {name} — {personality}")

    @commands.command(name="resetcats")
    async def resetcats(self, ctx: commands.Context):
        """(Mod) Clear adoption status (keeps roster)."""
        if not self.is_mod_or_broadcaster(ctx):
            return
        cats = load_cats()
        for c in cats:
            c["adopted_by"] = None
        save_cats(cats)
        await ctx.send("All cats are now available for adoption again! 🐾")

def prepare(bot: commands.Bot):
    # Called by bot.load_module("cogs.cats") in TwitchIO 2.9.1
    bot.add_cog(Cats(bot))
