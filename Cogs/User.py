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

class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["profile", "u"])
    async def user(self, ctx, user : Union[discord.User, str] = None):
        """View the discord.bio profile of a user."""
        user = user if user else ctx.author
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.discord.bio/user/details/{ user if isinstance(user, str) else user.id }") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    data = data["payload"]
                    try:
                        user = await self.bot.fetch_user(int(data["discord"]["id"])) if isinstance(user, str) else user
                    except discord.NotFound:
                        user = user
                    embed = discord.Embed(
                        url = f"https://discord.bio/p/{ data['user']['details']['slug'] }",
                        description = f"{ Config.EMOTES['pencil'] } **Description:** {data['user']['details']['description']}\n{ Config.EMOTES['heart'] } **Likes:** { data['user']['details']['likes'] }",
                        color = embed_color(ctx.author) if ctx.guild else Config.MAINCOLOR
                    )
                    try:
                        embed.title = f"{ user } `({data['user']['details']['slug']})`{ ' ' + Config.EMOTES['diamond'] if data['user']['details']['premium'] else '' }{ ' ' + Config.EMOTES['gavel'] if data['user']['details']['staff'] else '' }{ ' ' + Config.EMOTES['settings'] if user.id in Config.OWNERIDS else '' }"
                    except KeyError:
                        embed.title = f"{ user } `({data['user']['details']['slug']})`{ ' ' + Config.EMOTES['diamond'] if data['user']['details']['premium'] else '' }{ ' ' + Config.EMOTES['settings'] if user.id in Config.OWNERIDS else '' }"
                    embed.set_thumbnail(url = user.avatar_url)
                    if data["user"]["details"]["banner"]:
                        embed.set_image(url = data["user"]["details"]["banner"])
                    if data["user"]["details"]["birthday"]:
                        birthdate = datetime.datetime.strptime(data["user"]["details"]["birthday"], "%Y-%m-%d")
                        embed.description += f"\n{ Config.EMOTES['cake'] } **Birthdate:** { birthdate.strftime('%A, %B %d, %Y')}"
                    connections = ""
                    if data["user"]["discordConnections"]:
                        i = 0
                        for connection in data["user"]["discordConnections"]:
                            connection = list(connection.keys())[0]
                            if connection == "github":
                                connections += f"[{ Config.EMOTES[connection] }](https://github.com/{ data['user']['discordConnections'][i][connection]['name'] })"
                            elif connection == "reddit":
                                connections += f"[{ Config.EMOTES[connection] }](https://reddit.com/u/{ data['user']['discordConnections'][i][connection]['name'] })"
                            elif connection == "steam":
                                connections += f"[{ Config.EMOTES[connection] }](https://steamcommunity.com/profiles/{ data['user']['discordConnections'][i][connection]['id'] })"
                            elif connection == "twitch":
                                connections += f"[{ Config.EMOTES[connection] }](https://twitch.tv/{ data['user']['discordConnections'][i][connection]['name'] })"
                            elif connection == "twitter":
                                connections += f"[{ Config.EMOTES[connection] }](https://twitter.com/{ data['user']['discordConnections'][i][connection]['name'] })"
                            elif connection == "spotify":
                                connections += f"[{ Config.EMOTES[connection] }](https://open.spotify.com/user/{ data['user']['discordConnections'][i][connection]['id']})"
                            i += 1
                    if data["user"]["userConnections"]:
                        for connection in data["user"]["userConnections"]:
                            if connection == "website":
                                connections += f"[{ Config.EMOTES[connection] }]({ 'https://' if data['user']['userConnections'][connection].startswith('https://') == False and data['user']['userConnections'][connection].startswith('https://') == False else '' }{ data['user']['userConnections'][connection] })"
                            elif connection == "instagram":
                                connections += f"[{ Config.EMOTES[connection] }](https://instagram.com/{ data['user']['userConnections'][connection] })"
                            elif connection == "snapchat":
                                connections += f"[{ Config.EMOTES[connection] }](https://www.snapchat.com/add/{ data['user']['userConnections'][connection] })"
                            elif connection == "linkedin":
                                connections += f"[{ Config.EMOTES[connection] }](https://www.linkedin.com/in/{ data['user']['userConnections'][connection] })"
                    if connections != "":
                        embed.description += f"\n{ Config.EMOTES['website'] } **Connections:** { connections }"
                    if data["user"]["details"]["email"]:
                        embed.description += f"\n{ Config.EMOTES['envelope'] } **Email:** { data['user']['details']['email'] }"
                    if data["user"]["details"]["gender"]:
                        if data["user"]["details"]["gender"] == 0:
                            embed.description += f"\n{ Config.EMOTES['gender'] } **Gender:** Male"
                        else:
                            embed.description += f"\n{ Config.EMOTES['gender'] } **Gender:** { 'Female' if data['user']['details']['gender'] == 1 else 'Nonbinary' }"
                    if data["user"]["details"]["location"]: 
                        embed.description += f"\n{ Config.EMOTES['map'] } **Location:** { data['user']['details']['location'] }"
                    if data["user"]["details"]["occupation"]:
                        embed.description += f"\n{ Config.EMOTES['briefcase'] } **Occupation:** { data['user']['details']['occupation'] }"
                elif resp.status == 401:
                    embed = discord.Embed(
                        title = "Empty Argument",
                        description = "Please provide a user or a slug to view!",
                        color = Config.ERRORCOLOR
                    )
                elif resp.status == 404:
                    embed = discord.Embed(
                        title = "Invalid Argument",
                        description = "Please provide a valid user or a slug to view!",
                        color = Config.ERRORCOLOR
                    )
                await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(User(bot))