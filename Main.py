# Imports
import asyncio
import datetime
import logging
import random

import discord
import pymongo
from discord.ext import commands

import Config

# Logging system setup
logging.basicConfig(level = logging.INFO, format="discord.bio | [%(levelname)s] | %(message)s")

async def get_prefix(bot, message):
    # If the command wasn't used in a server it returns the default prefix
    if message.guild is None:
        return commands.when_mentioned_or(Config.PREFIX)(bot, message)
    else:
        # Gets all the prefixes from the databse
        prefix = Config.CLUSTER["servers"]["prefixes"].find_one(
            {"_id": message.guild.id})
        # If it can't find a prefix for the server the command was used in it returns the default prefix
        if prefix == None:
            return commands.when_mentioned_or(Config.PREFIX)(bot, message)
        else:
            # Returns custom prefix if it does exist
            return prefix["prefix"]

# Set prefix and set case insensitive to true so a command will work if miscapitlized
bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True)

# Remove default help command
bot.remove_command('help')

# Cogs
cogs = ["Other", "Bio"]

# Starts all cogs
for cog in cogs:
    bot.load_extension("Cogs." + cog)

# Check to see if the user invoking the command is in the OWNERIDS Config
def owner(ctx):
    return int(ctx.author.id) in Config.OWNERIDS

# Restarts and reloads all cogs
@bot.command()
@commands.check(owner)
async def restart(ctx):
    """
    Restart the bot.
    """
    embed = discord.Embed(
        color = Config.MAINCOLOR
    )
    embed.set_author(name = "Restarting")
    msg = await ctx.send(embed = embed)
    animate = ["Restarting", "Restarting.", "Restarting..", "Restarting..."]
    num = -1
    # Gets every cog from the cog list and restarts it
    for cog in cogs:
        if num == 3:
            num = 0
        else:
            num += 1
        bot.reload_extension("Cogs." + cog)
        embed.add_field(name = f"{cog}", value = "🔁 Restarted!")
        embed.set_author(name = animate[num])
        await msg.edit(embed = embed)
    logging.info(f"Bot has been restarted succesfully by {ctx.author.name}#{ctx.author.discriminator} (ID - {ctx.author.id})!")
    await asyncio.sleep(3)
    await msg.delete()
    if ctx.guild != None:
        try:
            await ctx.message.delete()
        except:
            pass

# Command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.BadArgument):
        pass
    else:
        raise error

# On ready
@bot.event
async def on_ready():
    logging.info(f"Bot has been started succesfully!")

    # Loop for status
    loop = True
    while loop == True:
        statuses = ["being developed by Polar!"]
        await bot.change_presence(activity = discord.Game(random.choice(statuses)))
        await asyncio.sleep(600)

# Starts bot
bot.run(Config.TOKEN)
