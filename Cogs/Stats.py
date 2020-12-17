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
import os, platform
from datetime import datetime
## Packages that have to be installed through the package manager.
import discord, psutil
from discord.ext import commands
## Packages on this machine.
import Config
from Utils import embed_color, __version__

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["info"])
    async def stats(self, ctx):
        """View some detailed statistics about the bot."""
        commands = 0
        for COG in Config.COGS:
            commands += len(set(self.bot.cogs[COG].walk_commands()))
        channels = 0
        roles = 0
        for guild in self.bot.guilds:
            channels += len(guild.channels)
            roles += len(guild.roles)
        process = psutil.Process(os.getpid())
        total_mem = psutil.virtual_memory().total
        current_mem = process.memory_info().rss
        name = f"{self.bot.user.name}'" if self.bot.user.name[-1] == "s" else f"{self.bot.user.name}'s"
        embed = discord.Embed(
            title = f"{name} Statistics",
            timetamp = datetime.utcnow(),
            color = embed_color(ctx.author) if ctx.guild else Config.MAINCOLOR
        )
        embed.add_field(name = "📊 Bot Statistics", value = f"**Servers:** {len(self.bot.guilds)}\n**Users:** {len(self.bot.users)}\n**Channels:** {channels}\n**Roles:** {roles}\n**Shards:** {self.bot.shard_count} `[ID: {(ctx.guild.shard_id if ctx.guild else 0) + 1}]`", inline = False)
        embed.add_field(name = "📋 Bot Information", value = f"**Creator:** [**Polar#6880**](https://discord.com/users/619284841187246090)\n**Bot Version:** {__version__}\n**Lines of Code:** 870\n**Commands:** {commands}")
        embed.add_field(name = "🖥 Hardware", value = f"**discord.py Version:** v{discord.__version__}\n**Python Version:** {platform.python_version()}\n**Operating System:** {platform.system()} {platform.release()} {platform.version()}\n**Memory Usage:** {(current_mem / total_mem) * 100:.2f}% ({process.memory_info().rss / 1000000:.2f}mb)", inline = False)
        await ctx.send(embed = embed)
            
def setup(bot):
    bot.add_cog(Stats(bot))