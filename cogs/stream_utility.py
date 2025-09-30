# Most stream utilities will be consolidated here.
import datetime
from twitchio.ext import commands

def format_timedelta(delta: datetime.timedelta) -> str:
    seconds = int(delta.total_seconds())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    if not parts:
        return "just now"
        
    return ", ".join(parts)


class StreamUtility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="followage")
    async def followage(self, ctx: commands.Context, user: str = None):

        target_username = user.strip('@') if user else ctx.author.name
        
        try:
            target_user = await self.bot.fetch_users(names=[target_username])
            if not target_user:
                return await ctx.send(f"User '{target_username}' not found.")
            target_user = target_user[0]
        except Exception as e:
            print(f"Error fetching user: {e}")
            return await ctx.send("Could not fetch user data from Twitch.")
            
        channel = ctx.channel

        try:
            follow = await target_user.fetch_follow(channel.name)
        except Exception as e:
            print(f"Error fetching follow data: {e}")
            return await ctx.send("Could not fetch follow data from Twitch.")

        if follow is None:
            return await ctx.send(f"@{target_username} is not following {channel.name}.")
            
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        follow_duration = now_utc - follow.followed_at
        
        duration_str = format_timedelta(follow_duration)
        await ctx.send(f"@{target_username} has been following me for {duration_str}. Thanks for the support! ❤️")


def prepare(bot: commands.Bot):
    bot.add_cog(StreamUtility(bot))