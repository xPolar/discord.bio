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
## Packages that have to be installed through the package manager.
import discord
from discord.ext import commands
## Packages on this machine.
import Config
from Utils import embed_color, get_prefix

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    def command_help(self, ctx, name : str, description : str, usage : str, aliases : list = None):
        """Generate a help embed for commands.

        Args:
            ctx (discord.Context): discord.py's context object.
            name (str): The name of the command.
            description (str): The of the command.
            usage (str): How to use the command.
            aliases (str, optional): If there are any aliases to the command. Defaults to None.

        Returns:
            discord.Embed: The generated embed.
        """
        embed = discord.Embed(
            title = name,
            description = description,
            color = embed_color(ctx.author) if ctx.guild else Config.MAINCOLOR
        )
        embed.set_author(name = "Command Help", icon_url = "https://cdn.discordapp.com/emojis/512367613339369475.png?width=834&height=834")
        embed.description = embed.description + f"\n\nPlease do: `{usage}`"
        if aliases:
            embed.description = embed.description + "\n\nAliases: " + ", ".join([ f'`{alias}`' for alias in aliases ])
        return embed
    
    @commands.group()
    async def help(self, ctx):
        """View the help menu or information on a certain command."""
        if ctx.invoked_subcommand == None:
            prefix = get_prefix(ctx.message)
            embed = discord.Embed(
                color = embed_color(ctx.author) if ctx.guild else Config.MAINCOLOR   
            )
            embed.set_author(name = "Command Help", icon_url = "https://cdn.discordapp.com/emojis/512367613339369475.png?width=834&height=834")
            embed.add_field(name = "Help", value = f"`{prefix}help [Command]`\n*View the help menu or information on a certain command.*", inline = False)
            embed.add_field(name = "Links", value = f"`{prefix}links`\n*Obtain all of the important links.*", inline = False)
            embed.add_field(name = "Ping", value = f"`{prefix}ping`\n*Get the latency between our bot and Discord as well as the latency of the host.*", inline = False)
            embed.add_field(name = "Prefix", value = f"`{prefix}prefix [New Prefix]`\n*View or set a prefix within a server.*", inline = False)
            if ctx.author.id in Config.OWNERIDS:
                embed.add_field(name = "Restart", value = f"`{prefix}restart`\n*Restart the bot's cogs.*", inline = False)
            embed.add_field(name = "Stats", value = f"`{prefix}stats`\n*View some detailed statistics about the bot.*", inline = False)
            embed.add_field(name = "Top", value = f"`{prefix}top`\n*View the top profiles on [discord.bio](https://discord.bio/profiles).*", inline = False)
            embed.add_field(name = "User", value = f"`{prefix}user [User or Slug]`\n*View a [discord.bio](https://discord.bio) account.*", inline = False)
            await ctx.send(embed = embed)

    @help.command(name = "help")
    async def _help(self, ctx):
        await ctx.send(embed = self.command_help(ctx, "help", "View the help menu or information on a certain command.", "help [Command]"))
    
    @help.command()
    async def links(self, ctx):
        await ctx.send(embed = self.command_help(ctx, "links", "Obtain all of the important links.", "links"))

    @help.command()
    async def ping(self, ctx):
        await ctx.send(embed = self.command_help(ctx, "ping", "Get the latency between our bot and Discord as well as the latency of the host.", "ping"))
    
    @help.command()
    async def prefix(self, ctx):
        await ctx.send(embed = self.command_help(ctx, "prefix", "View or set a prefix within a server.", "prefix [New Prefix]"))
    
    @help.command()
    async def restart(self, ctx):
        if ctx.author.id in Config.OWNERIDS:
            await ctx.send(embed = self.command_help(ctx, "restart", "Restart the bot's cogs.", "restart"))
    
    @help.command()
    async def stats(self, ctx):
        await ctx.send(embed = self.command_help(ctx, "stats", "View some detailed statistics about the bot.", "stats"))
    
    @help.command()
    async def top(self, ctx):
        await ctx.send(embed = self.command_help(ctx, "top", "View the top profiles on [discord.bio](https://discord.bio/profiles).", "top"))
    
    @help.command(aliases = ["profile", "u"])
    async def user(self, ctx):
        await ctx.send(embed = self.command_help(ctx, ctx.invoked_with.lower(), f"View a user's [discord.bio](https://discord.bio) profile.", f"{ ctx.invoked_with.lower() } <User or Slug>", ["u" if ctx.invoked_with.lower() == "user" else "user", "profile"] if ctx.invoked_with.startswith("u") else ["u", "user"]))

def setup(bot):
    bot.add_cog(Help(bot))
