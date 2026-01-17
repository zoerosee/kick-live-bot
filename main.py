
import discord
from discord import app_commands
from discord.ext import commands
import requests
from flask import Flask
from threading import Thread
import os

# ----------------------------
# BOT TOKEN
# ----------------------------
TOKEN = "MTQ2MjE4NjY2NjIwOTg0MTE4Mg.GIHY3E.CUDK0iSFdD0jBwNRRWSa4crg12JRb7W-JtqfXE"  # <-- Replace with your bot token

# ----------------------------
# Load streamers from file
# ----------------------------
STREAMERS_FILE = "streamers.txt"

if not os.path.exists(STREAMERS_FILE):
    with open(STREAMERS_FILE, "w") as f:
        f.write("xqc\ndestiny\n")  # default list

with open(STREAMERS_FILE, "r") as f:
    KICK_STREAMERS = [line.strip().lower() for line in f if line.strip()]

# ----------------------------
# BOT SETUP
# ----------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# ----------------------------
# /live command
# ----------------------------
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

# ----------------------------
# /add_streamer command
# ----------------------------
@bot.tree.command(name="add_streamer", description="Add a Kick streamer to track")
@app_commands.describe(username="Kick username to add")
async def add_streamer(interaction: discord.Interaction, username: str):
    username = username.lower()
    if username in KICK_STREAMERS:
        await interaction.response.send_message(f"❌ {username} is already being tracked.")
    else:
        KICK_STREAMERS.append(username)
        with open(STREAMERS_FILE, "a") as f:
            f.write(username + "\n")
        await interaction.response.send_message(f"✅ Added {username} to tracked streamers.")

# ----------------------------
# /remove_streamer command
# ----------------------------
@bot.tree.command(name="remove_streamer", description="Remove a Kick streamer from the list")
@app_commands.describe(username="Kick username to remove")
async def remove_streamer(interaction: discord.Interaction, username: str):
    username = username.lower()
    if username not in KICK_STREAMERS:
        await interaction.response.send_message(f"❌ {username} is not in the tracked list.")
    else:
        KICK_STREAMERS.remove(username)
        with open(STREAMERS_FILE, "w") as f:
            for s in KICK_STREAMERS:
                f.write(s + "\n")
        await interaction.response.send_message(f"✅ Removed {username} from tracked streamers.")

# ----------------------------
# KEEP-ALIVE WEB SERVER
# ----------------------------
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"
def run():
    app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# ----------------------------
# RUN BOT
# ----------------------------
bot.run(TOKEN)
