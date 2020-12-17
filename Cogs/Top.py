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
from typing import Union
## Packages that have to be installed through the package manager.
import aiohttp, discord
from discord.ext import commands
## Packages on this machine.
import Config
from Utils import embed_color

class Top(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def top(self, ctx, user : Union[discord.User, str] = None):
        """View the top profiles on [discord.bio](https://discord.bio/profiles)."""
        user = user if user else ctx.author
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.discord.bio/user/top") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    data = data["payload"]
                    i = 1
                    list = []
                    for user in data["users"]:
                        if i <= 10:
                            list.append(f"**{ i }. [dsc.bio/{ user['user']['slug']}](https://discord.bio/p/{ user['user']['slug'] }):** { user['user']['likes'] } likes")
                        else:
                            break
                        i += 1
                    embed = discord.Embed(
                        title = "Top Liked Users",
                        description = "\n".join(list),
                        color = embed_color(ctx.author) if ctx.guild else Config.MAINCOLOR
                    )
                    embed.set_thumbnail(url = "https://cdn.discordapp.com/emojis/788292835782426626.png?v=1")
                else:
                    embed = discord.Embed(
                        title = "Error",
                        description = f"**```\nuser/top returned error code: { resp.status }\n```**",
                        color = Config.ERRORCOLOR
                    )
                    embed.set_footer(text = "Please report this to Polar#6880")
                await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Top(bot))