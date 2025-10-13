import os
import json
import sys 
from twitchio.ext import commands
from dotenv import load_dotenv
from cogs.basic import commands_list


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")

try:
    with open("auth/token.json") as f:
        token_data = json.load(f)
except FileNotFoundError:
    print("FATAL: auth/token.json not found. Please run get_token.py to generate it.")
    sys.exit(1)

if not CLIENT_ID:
    print("----------------------------------------------------------------")
    print("         CLIENT_ID isn't set in environment variables. Please reach out to programmer hubby.")
    print("         The !followage command will not work.")
    print("         To fix this, create a .env file or set the variable.")
    print("----------------------------------------------------------------")

class VyleyBot(commands.Bot):
    def __init__(self):
        print("🔧 Initializing bot...")
        super().__init__(
            token=token_data["access_token"],
            prefix="!",
            initial_channels=["theterribleplayer"],
        )
        
        self.client_id = CLIENT_ID
        self.token = token_data["access_token"]
        
        for cmd in commands_list:
            self.add_command(cmd)
        print("🔧 Bot initialized!")

    async def event_ready(self):
        print(f"✅ VyleyBot is connected to Twitch as {self.nick}")
        print(f"📦 Registered commands: {[c.name for c in self.commands.values()]}")

    async def event_message(self, message):
        print("⚡ TRIGGERED: event_message")
        print(f"RAW MESSAGE: {message.content} from {getattr(message.author, 'name', 'unknown')}")
        if message.echo:
            print("⏭️ Ignoring echo message")
            return
        print(f"[CHAT LOG] {getattr(message.author, 'name', 'unknown')}: {message.content}")
        print("✅ Calling handle_commands")
        await self.handle_commands(message)

    async def event_error(self, error, data=None):
        print(f"❌ EVENT ERROR: {error}")
        if data:
            print(f"📝 DATA: {data}")

if __name__ == "__main__":
    bot = VyleyBot()
    print("🚀 Running bot...")
    bot.load_module("cogs.cats")
    print("🐈 Cats to Adopt... Enabled!")
    bot.load_module("cogs.quotes")
    print("📝 Quotes module... Enabled!")
    bot.load_module("cogs.welcome")
    print("👋 Welcome new chatters... Enabled!")
    bot.load_module("cogs.stream_utility")
    print("📊 Stream Utility commands... Enabled!")
    bot.load_module("cogs.counters")
    print("🧮 Counter commands... Enabled!")
    bot.run()
