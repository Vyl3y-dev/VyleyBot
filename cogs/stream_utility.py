import datetime
import iso8601
import aiohttp # Needed cause twitchIO sucks.
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
        return "a few moments"
        
    if len(parts) > 1:
        return f"{', '.join(parts[:-1])} and {parts[-1]}"
        
    return parts[0]


class StreamUtility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_follow_since(self, user_id: str, broadcaster_id: str) -> datetime.datetime | None:

        headers = {
            'Client-ID': self.bot.client_id,  # Correctly access the client_id
            'Authorization': f'Bearer {self.bot.token}'
        }
        
        url = f'https://api.twitch.tv/helix/channels/followers?user_id={user_id}&broadcaster_id={broadcaster_id}'
        
        # We create a new, temporary session to make our own web request.
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data'):
                        follow_date_str = data['data'][0]['followed_at']
                        return iso8601.parse_date(follow_date_str)
                else:
                    # Fuck twitch API, they make it so difficult to get simple data.
                    print(f"[API ERROR] Twitch returned status {response.status}: {await response.text()}")
                return None

    @commands.command(name="followage")
    async def followage(self, ctx: commands.Context, user: str = None):
        
        target_username = user.strip('@') if user else ctx.author.name
        
        try:
            target_user_list = await self.bot.fetch_users(names=[target_username])
            if not target_user_list:
                return await ctx.send(f"User '{target_username}' not found on Twitch.")
            target_user = target_user_list[0]
            
            broadcaster_list = await self.bot.fetch_users(names=[ctx.channel.name])
            if not broadcaster_list:
                return await ctx.send("An error occurred: Could not find the broadcaster.")
            broadcaster = broadcaster_list[0]

            follow_since = await self.get_follow_since(target_user.id, broadcaster.id)

        except Exception as e:
            print(f"An unexpected error occurred in followage command: {e}")
            return await ctx.send("An unexpected error occurred while checking followage.")

        if follow_since is None:
            return await ctx.send(f"@{target_username} is not following {ctx.channel.name}.")
            
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        follow_duration = now_utc - follow_since
        
        duration_str = format_timedelta(follow_duration)
        await ctx.send(f"@{target_username} has been following {ctx.channel.name} for {duration_str}. Thanks for the support! ❤️")


def prepare(bot: commands.Bot):
    bot.add_cog(StreamUtility(bot))