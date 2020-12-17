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
import time
## Packages that have to be installed through the package manager.
import discord
from colorama import Fore, Style
from discord.ext import commands
## Packages on this machine.
import Config
from Utils import embed_color

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["latency"])
    async def ping(self, ctx):
        """Get the latency between our bot and Discord as well as the latency of the host."""

        # Get the time at one point, trigger typing, get the time again then subtract the two values to get the host latency. To get API latency use self.bot.latency, get round trip by adding up the two latencies.
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(
            title = "🏓 Pong!",
            description = f"Host latency is { round((t2 - t1) * 1000) }ms.\nAPI latency is { int(round(self.bot.latency * 1000, 2)) }ms.\nRound Trip took { int(round((t2 - t1) * 1000) + round(self.bot.latency * 1000, 2)) }ms.",
            color = embed_color(ctx.author) if ctx.guild != None else Config.MAINCOLOR
        )

        # Print out into the console when the round trip takes over 500 milliseconds.
        if round((t2 - t1) * 1000) + round(self.bot.latency * 1000, 2) > 500:
            print()
            print(f"{Style.BRIGHT}{Fore.RED}[WARNING]{Fore.WHITE} API latency is { round((t2 - t1) * 1000) }ms, host latency is { int(round(self.bot.latency * 1000, 2)) }ms, and round trip took { int(round((t2 - t1) * 1000) + round(self.bot.latency * 1000, 2)) }ms.")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Ping(bot))