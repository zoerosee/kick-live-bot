import discord
import requests
from discord import app_commands
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

TOKEN = "MTQ2MjE4NjY2NjIwOTg0MTE4Mg.GDaAb7.eyObdkQh3wNHuKrDvPmulEKaRtga7QO17iVeJs"  # Replace with your actual Discord token

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

# Tiny web server to keep the bot awake
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"
def run():
    app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

bot.run(TOKEN)
