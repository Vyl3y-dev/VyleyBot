import os
import json
import sys 
import io
from twitchio.ext import commands
from dotenv import load_dotenv
from cogs.basic import commands_list
import subprocess
import threading
import asyncio
from eventsub_workingtest import listen_eventsub

sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")

# --- Load Bot Token ---
try:
    with open("auth/token_bot.json") as f:
        token_data = json.load(f)
except FileNotFoundError:
    print("FATAL: auth/token_bot.json not found. Run: python get_token.py bot")
    sys.exit(1)

if not CLIENT_ID:
    print("----------------------------------------------------------------")
    print("  CLIENT_ID isn't set in environment variables.")
    print("  The !followage command and Twitch API calls may fail.")
    print("----------------------------------------------------------------")

# Optional: check broadcaster token exists
if not os.path.exists("auth/token_broadcaster.json"):
    print("⚠️  Broadcaster token not found — EventSub events unavailable.")
else:
    print("✅ Broadcaster token found.")


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
# === Start EventSub listener as background process and capture output ===
    def run_eventsub():
        asyncio.run(listen_eventsub())

    print("🧠 Launching EventSub listener in background...")
    eventsub_path = os.path.join(os.path.dirname(__file__), "eventsub_workingtest.py")

    eventsub_proc = subprocess.Popen(
        [sys.executable, "-u", eventsub_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    # Thread to forward EventSub output into VyleyBot's console
    def forward_eventsub_output():
        while True:
            line = eventsub_proc.stdout.readline()
            if not line:
                break
            print(f"[EventSub] {line}", end="", flush=True)

    threading.Thread(target=forward_eventsub_output, daemon=True).start()

    # === Load cogs and start bot ===
    print("🚀 Running bot...")
    bot.load_module("cogs.cats");        print("🐈 Cats to Adopt... Enabled!")
    bot.load_module("cogs.quotes");      print("📝 Quotes module... Enabled!")
    bot.load_module("cogs.welcome");     print("👋 Welcome new chatters... Enabled!")
    bot.load_module("cogs.stream_utility"); print("📊 Stream Utility commands... Enabled!")
    bot.load_module("cogs.counters");    print("🧮 Counter commands... Enabled!")
    bot.load_module("cogs.position");    print("🥇 Position commands... Enabled!")

    bot.run()
