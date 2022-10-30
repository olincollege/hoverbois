"""
Discord bot to report IP address of Rasp Pi.
"""

import os
from getpass import getuser
import socket

import discord
from discord.ext import commands

# from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver

# Setup bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

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

    await ctx.send(f"ip: `{ip}` link: http://{ip}:8888")


@bot.command()
async def pwd(ctx):
    """
    Print the working directory of the program.

    This is for debugging purposes.

    Args:
        ctx: Discord context
    """
    path = os.getcwd()
    await ctx.send(f"path: {path}")


@bot.command()
async def whoami(ctx):
    """
    Print the user running the bot process.

    This is for debugging purposes.

    Args:
        ctx: Discord context
    """
    user = getuser()
    await ctx.send(f"username: {user}")


def main():
    """
    Main loop
    """
    # Get botkey from CLI arg (argparse is better but this works)
    import sys
    botkey = sys.argv[1]
    bot.run(botkey)


if __name__ == "__main__":
    main()
