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
## Packages default to Python.
import datetime
from asyncio import sleep
## Packages that have to be installed through the package manager.
import aiohttp, discord
from colorama import Fore, Style, init
from discord.ext import commands
## Packages on this machine.
import Config
from Utils import embed_color, get_prefix as gp, load_prefixes

# Initialize colorama
init()

def get_prefix(bot, message):
    """Returns the bot's prefix.

    Args:
        bot (commands.AutoShardedBot): The bot object.
        message (discord.Message): Message object.

    Returns:
        str: The prefix the bot will accept.
    """
    return commands.when_mentioned_or(gp(message))(bot, message)

intents = discord.Intents.default()
intents.members = True
bot = commands.AutoShardedBot(command_prefix = get_prefix, case_insensitive = True, intents = intents)

# Load all of the custom prefixes into the "cache".
load_prefixes()

# Remove our help command
bot.remove_command("help")

# Loads all of our cogs.
for COG in Config.COGS:
    bot.load_extension(f"Cogs.{COG}")
    print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Loaded Cog: {COG}")

async def owner(ctx):
    """Checks if a user is allowed to run the restart.

    Args:
        ctx (discord.py's context object): Context object.

    Returns:
        bool: Wether the user is one of the bot's owners.
    """
    return ctx.author.id in Config.OWNERIDS

@bot.command()
@commands.check(owner)
async def restart(ctx):
    """Restart the bot's cogs."""
    embed = discord.Embed(
        title = "Bot Restarted",
        color = Config.MAINCOLOR if ctx.guild == None else embed_color(ctx.author)
    )
    # Print a new line and then reload each cog, as well as print that each cog has been reloaded, then print out that the bot has been fully reloaded.
    print()
    for COG in Config.COGS:
        bot.reload_extension(f"Cogs.{COG}")
        print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Reloaded Cog: {COG}")
    await ctx.send(embed = embed)
    print(f"{Style.BRIGHT}{Fore.CYAN}[BOT-RESTARTED]{Fore.WHITE} Restart by {ctx.author} - {ctx.author.id}, I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")

@bot.event
async def on_command_error(ctx, error):
    """Error Handler."""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BadArgument):
        return
    elif isinstance(error, commands.CheckFailure):
        return
    elif isinstance(error, commands.BadUnionArgument):
        return
    elif isinstance(error, commands.BotMissingPermissions):
        return
    else:
        try:
            embed = discord.Embed(
                    title = "Error",
                    description = f"**```\n{error}\n```**".replace(Config.TOKEN, "[ R E D A C T E D ]"),
                    color = Config.ERRORCOLOR
            )
            embed.set_footer(text = "Please report this to Polar#6880")
            await ctx.send(embed = embed)
        finally:
            raise error

@bot.event
async def on_guild_join(guild):
    """When the bot joins a server send a webhook with detailed information as well as print out some basic information."""
    embed = discord.Embed(
        title = "Joined a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0x77DD77
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members) - 1)
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner", value = f"{guild.owner.name}#{guild.owner.discriminator}")
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(Config.WEBHOOK, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Joined a server")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[JOINED-SERVER]{Fore.WHITE} Joined {Fore.YELLOW}{guild.name}{Fore.WHITE} with {Fore.YELLOW}{len(guild.members) - 1}{Fore.WHITE} members.")

@bot.event
async def on_guild_remove(guild):
    """When the bot leaves a server send a webhook with detailed information as well as print out some basic information."""
    embed = discord.Embed(
        title = "Left a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0xFF6961
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members))
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner", value = f"{guild.owner.name}#{guild.owner.discriminator}")
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(Config.WEBHOOK, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Left a server")
    print(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}[LEFT-SERVER]{Fore.WHITE} Left {Fore.YELLOW}{guild.name}{Fore.WHITE} with {Fore.YELLOW}{len(guild.members)}{Fore.WHITE} members.")

@bot.event
async def on_shard_ready(shard_id):
    """When a shard starts print out that the shard has started.

    Args:
        shard_id (int): The ID of the shard that has started. (Starts from 0).
    """
    print(f"{Style.BRIGHT}{Fore.CYAN}[SHARD-STARTED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has started!")

@bot.event
async def on_ready():
    """When the bot fully starts print out that the bot has started and set the status."""
    print(f"{Style.BRIGHT}{Fore.CYAN}[BOT-STARTED]{Fore.WHITE} I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")
    while True:
        await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(f"with {Config.PREFIX}help"))
        await sleep(1800)

# Start the bot.
bot.run(Config.TOKEN)