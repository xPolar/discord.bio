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
from Utils import embed_color, get_prefix, prefixes

class Prefixes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def prefix(self, ctx, new_prefix = None):
        """View or set a prefix within a server."""
        if new_prefix == None or ctx.guild == None:
            embed = discord.Embed(
                description = f"Hey there, my name is { self.bot.user.name if ctx.guild == None else ctx.guild.me.display_name } and my prefix is `{ get_prefix(ctx.message) }`",
                color = embed_color(ctx.author) if ctx.guild != None else Config.MAINCOLOR
            )
        else:
            if ctx.author.guild_permissions.manage_guild == False:
                embed = discord.Embed(
                    title = "Missing Permissions",
                    description = "You're missing the **Manage Server** permission which is required to change a server's prefix!",
                    color = Config.ERRORCOLOR
                )
            else:
                if len(new_prefix) > 5 and new_prefix.lower() != "remove":
                    embed = discord.Embed(
                        title = "Prefix Too Long",
                        description = "Please keep the prefix under five characters long!",
                        color = Config.ERRORCOLOR
                    )
                else:
                    embed = discord.Embed(
                        title = f"Prefix Updated",
                        description = f"My prefix is now `{ new_prefix if new_prefix.lower() != 'remove' else Config.PREFIX }`",
                        color = embed_color(ctx.author)
                    )
                    Config.CLUSTER["servers"]["prefixes"].delete_one({"_id": ctx.guild.id}) if new_prefix.lower() == "remove" or new_prefix.lower() == Config.PREFIX else Config.CLUSTER["servers"]["prefixes"].update_one({"_id": ctx.guild.id}, {"$set": {"prefix": new_prefix}}, upsert = True)
                    if (new_prefix.lower() == "remove" or new_prefix.lower() == Config.PREFIX) and ctx.guild.id in prefixes:
                        if ctx.guild.me.guild_permissions.change_nickname:
                            await ctx.guild.me.edit(nick = ctx.guild.me.display_name.replace(f"[{ get_prefix(ctx.message) }]", ""))
                        prefixes.pop(ctx.guild.id)
                    else:
                        if ctx.guild.me.guild_permissions.change_nickname:
                            await ctx.guild.me.edit(nick = ctx.guild.me.display_name.replace(f"[{ get_prefix(ctx.message) }]", f"[{ new_prefix }]") if f"[{ get_prefix(ctx.message) }]" in ctx.guild.me.display_name else f"[{ new_prefix }] { ctx.guild.me.display_name }")
                        prefixes[ctx.guild.id] = new_prefix
        await ctx.send(embed = embed)
            
def setup(bot):
    bot.add_cog(Prefixes(bot))