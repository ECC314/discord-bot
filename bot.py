import discord
import asyncio
import logging
from sys import argv

logging.basicConfig(level=logging.INFO)

client = discord.Client()
if (len(argv) != 2):
    print("Usage: python3.5 discordbot.py channelid")
    exit()
channelid = int(argv[1])
print("Initialized in channel {}.".format(channelid))

@client.event
async def on_ready():
    print("Logged in as {}.".format(client.user.name))

@client.event
async def on_member_ban(guild, member):
    async for log in guild.audit_logs():
        if (log.action == discord.AuditLogAction.ban):
            message = "{} banned {}.".format(log.user.name, member.name)
            print(message)
            await client.get_channel(channelid).send(message)
            break

@client.event
async def on_member_unban(guild, member):
    async for log in guild.audit_logs():
        if (log.action == discord.AuditLogAction.unban):
            message = "{} unbanned {}.".format(log.user.name, member.name)
            print(message)
            await client.get_channel(channelid).send(message)
            break

client.run('auth-token')
