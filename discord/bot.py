"""
Discord bot to report IP address of Rasp Pi.
"""

import socket

import discord
from discord.ext import commands

# Setup bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load Discord API bot key.
# Probably better to use environment variables or CLI flags but whatever
from botkey import botkey

# Setup commands

@bot.command()
async def ip(ctx):
    """
    Get the local IP addr and print it.

    Args:
        ctx: Discord context
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('10.0.0.0', 0))
        ip = s.getsockname()[0]

    await ctx.send(f"ip: `{ip}`")


# Run
bot.run(botkey)
