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

# IMPORTANT
# Whenever you edit the Config file you must do a full restart of the bot (This also applies if you edit the main file)
# IMPORTANT

# Packages
## Packages that have to be installed through the package manager.
import pymongo

# Discord Bot
## Bot's token (DON'T SHARE WITH ANYONE ELSE!) (To find your token go to https://discordapp.com/developers/applications/ > Your Bot's Application > Bot (Turn the application into a bot if you haven't already) > Token)
TOKEN = ""
## Bot's prefix
PREFIX = "!"
## Owner IDS (People who have access to restart the bot)
OWNERIDS = [619284841187246090]
## Main Color (Replace the part after 0x with a hex code)
MAINCOLOR = 0x2F3136
## Error Color (Replace the part after the 0x with a hex code)
ERRORCOLOR = 0xFF3F3F
## Webhook URL (For join / leave logs)
WEBHOOK = ""
## All of the cogs within the bot that we want to load.
COGS = ["Prefixes", "User", "Stats", "Ping", "Help", "Top", "Links"]
## EMOTES, MAKE SURE TO REPLACE ALL OF THESE WITH VALID DISCORD EMOJIS
EMOTES = {"pencil": "", "diamond": "", "gavel": "", "heart": "", "settings": "", "map": "", "cake": "", "briefcase": "", "envelope": "", "gender": "", "website": "", "instagram": "<:instagr", "snapchat": "", "linkedin": "", "github": "", "reddit": "", "steam": "", "twitch": "", "battlenet": "", "spotify": "", "twitter": ""}

# MongoDB
## Cluster (Replace the <password> of your uri part with your password and remove the "<>")
CLUSTER = pymongo.MongoClient("")