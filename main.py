import discord
import requests
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.environ['TOKEN']  # Token will be set in Railway

# List of Kick streamers
KICK_STREAMERS = [
    "xqc",
    "destiny",
    # add more here
]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="live", description="Show which tracked Kick streamers are live")
async def live(interaction: discord.Interaction):
    live_now = []
    for streamer in KICK_STREAMERS:
        url = f"https://kick.com/api/v2/channels/{streamer}"
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            if data.get("livestream"):
                live_now.append(streamer)
        except:
            pass

    if live_now:
        msg = "**🟢 Live on Kick:**\n" + "\n".join(f"• {s}" for s in live_now)
        
    else:
        msg = "🔴 No tracked streamers are live right now."
    await interaction.response.send_message(msg)

bot.run(TOKEN)
