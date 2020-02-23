# IMPORTANT
# Whenever you edit the Config file you must do a full restart of the bot (This also applies if you edit the main file)
# IMPORTANT

# Imports
import pymongo

# Discord Bot
# Bot's token (DON'T SHARE WITH ANYONE ELSE!) (To find your token go to https://discordapp.com/developers/appli~cations/ > Your Wumpus-Bot Application > Bot (Turn the application into a bot if you haven't already) > Token)
TOKEN = ""
# Bot's prefix
PREFIX = ""
# Owner IDS (People who have access to restart the bot)
OWNERIDS = []
# Main Color (Replace the part after 0x with a hex code)
MAINCOLOR = 0x
# Error Color (Replace the part after 0x with a hex code)
ERRORCOLOR = 0x

## MongoDB
# Cluster (Replace the <password> part of your uri with your password and remove the "<>")
CLUSTER = pymongo.MongoClient("")
