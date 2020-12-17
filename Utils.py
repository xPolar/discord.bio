"""
MIT License

Copyright (c) 2020 xPolar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Packages.
## Packages that have to be installed through the package manager.
import discord
from colorama import Style, Fore
## Packages on this machine.
import Config

# The version the bot is currently on, should change on every single update. 
__version__ = "v2.0.0"

# Prefix dictionary so I don't have to query database each time, now only have to make one query when the bot starts.
prefixes = {}

def embed_color(author : discord.Member):
    """Returns the rendered color of a member, if the rendred color is the default color return Config.MAINCOLOR.

    Args:
        author (discord.Member): Member object.

    Returns:
        0xFFFFFF or discord.Color: The color to return.
    """
    return Config.MAINCOLOR if author.color == discord.Color.default() else author.color

def load_prefixes():
    """Update our prefixes dictionary with all of our servers that have a custom prefix."""
    documents = Config.CLUSTER["servers"]["prefixes"].find({})
    for document in documents:
        prefixes[document["_id"]] = document["prefix"]
    print(f"{Style.BRIGHT}{Fore.YELLOW}[SUCCESS]{Fore.WHITE} Prefixes Loaded!")

def get_prefix(message : discord.Message):
    """Get the prefix for a server.

    Args:
        message (discord.Message): The message to check.

    Returns:
        str: The prefix that will work for the server.
    """
    global prefixes
    if message.guild == None:
        return Config.PREFIX
    else:
        return prefixes[message.guild.id] if message.guild.id in prefixes else Config.PREFIX