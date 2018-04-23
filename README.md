# Discord bot

## Requirements
- Python 3.5
- discord.py (`python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py`)

## Logged actions
- Ban/unban
- Kick (Not 100% reliable, see below)
- Mute/unmute
- Deafen/undeafen
- Deletion of someone else's chat message (Not 100% reliable, see below)

## Usage
```
$ python3 bot.py channel-id auth-token
```

## Known issues
1. If a moderator kicks player A and player B leaves the server before another activity created a new mod log entry, the bot will assume that player B has been kicked as well.
2. Message deletion alerts only work if the message was sent after the bot's last restart.
