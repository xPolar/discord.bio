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
from discord.ext import commands
## Packages on this machine.
import Config
from Utils import embed_color

class Links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def links(self, ctx):
        """Obtain all of the important links."""
        embed = discord.Embed(
            title = "Important Links",
            description = "**[Invite Link](https://discord.com/api/oauth2/authorize?client_id=675515934475288576&permissions=67488768&scope=bot)\n[discord.bio Official Server](https://discord.gg/QCA8RjA5RJ)\n[My GitHub](https://github.com/xPolar/discord.bio)**",
            color = embed_color(ctx.author) if ctx.guild else Config.MAINCOLOR
        )
        await ctx.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Links(bot))