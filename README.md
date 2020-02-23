# discord.bio
Repository for the unofficial [discord.bio](https://discord.bio) bot by [Polar](https://discord.bio/polar).

## Table of contents
- [Important Links]()
- [Commands]()
- [Self Hosting]()

### Important Links
- [Invite the bot](https://discordapp.com/api/oauth2/authorize?client_id=680334403876159488&permissions=378944&scope=bot)
- [Join the official discord.bio server](https://discord.gg/bio)

### Commands
| Command | Description | Usage |
| ------- | ----------- | ----- |
| d!profile | View the profile of a user on discord.bio. | d!profile <User ID or Slug> |
| d!leaderboard | View the top ten people on the discord.bio leaderboard, upvote wise. | d!leaderboard |
| d!help | Use the help command. | d!help [Command] |
| d!invite | View all of the links related to the bot | d!invite |
| d!ping | View the API latency and the host latency | d!ping |
| d!prefix | View or edit a server's preifx | d!prefix [Set or Reset] [New Preifx] |
| d!restart | Only avaliable if you're self hosting the bot. | d!restart |
  
### Self Hosting
While self hosting this bot please give the original author credit for their work.

#### Prerequisites
Before you can host the bot you're going to need a couple of things first. You'll first need to download [Python](https://www.python.org/downloads/) 3.6+ and add it to your path. After you install Python on your machine we'll need to download some Python libraries by doing the following commands in a terminal.
```
pip3 install dnspython
```
```
pip3 install pymongo
```
```
pip3 install discord.py
```
```
pip3 install aiohttp
```
#### Starting the bot
After downloading Python 3.6+ and all of the required libraries make sure you have the files downloaded and go to the directory where `Main.py` is located and do the following command to start the bot.
```
python3 Main.py
```
