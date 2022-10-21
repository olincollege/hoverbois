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
    # The following method might not work depending on how hostsfile is
    # configured. It's quick and dirty solution.
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    await ctx.send(f"hostname: {hostname}\nip: {ip}")


# Run
bot.run(botkey)
