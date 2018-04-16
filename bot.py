import discord
import asyncio
import logging
from sys import argv

logging.basicConfig(level=logging.INFO)

client = discord.Client()
if (len(argv) != 3):
    print("Usage: python3.5 discordbot.py channelid auth-token")
    exit()
channelid = int(argv[1])
print("Initialized in channel {}.".format(channelid))

@client.event
async def on_ready():
    print("Logged in as {}.".format(client.user.name))

# Log server bans.
@client.event
async def on_member_ban(guild, member):
    async for log in guild.audit_logs():
        if (log.action == discord.AuditLogAction.ban):
            message = "{} banned {}.".format(log.user.mention, member.mention)
            print(message)
            await client.get_channel(channelid).send(message)
            break

# Log server unbans.
@client.event
async def on_member_unban(guild, member):
    async for log in guild.audit_logs():
        if (log.action == discord.AuditLogAction.unban):
            message = "{} unbanned {}.".format(log.user.mention, member.mention)
            print(message)
            await client.get_channel(channelid).send(message)
            break

# Log server kicks.
@client.event
async def on_member_remove(member):
	log = await member.guild.audit_logs().__anext__();
	if (log.action == discord.AuditLogAction.kick):
		message = "{} kicked {}.".format(log.user.mention, member.mention)
		print(message)
		await client.get_channel(channelid).send(message)

# Log voicechat mute/deafen.
@client.event
async def on_voice_state_update(member, before, after):
	log = await member.guild.audit_logs().__anext__();
	if (log.action == discord.AuditLogAction.member_update):
		print(log)
		message = ""
		if (not before.mute and after.mute):
			message = "{} muted {} in #{}.".format(log.user.mention, member.mention, after.channel.name)
		if (before.mute and not after.mute):
			message = "{} unmuted {} in #{}.".format(log.user.mention, member.mention, after.channel.name)
		if (not before.deaf and after.deaf):
			message = "{} deafened {} in #{}.".format(log.user.mention, member.mention, after.channel.name)
		if (before.deaf and not after.deaf):
			message = "{} undeafened {} in #{}.".format(log.user.mention, member.mention, after.channel.name)
		if (message):
			await client.get_channel(channelid).send(message)

# Log deleted messages.
@client.event
async def on_message_delete(msg):
	log = await msg.guild.audit_logs().__anext__();
	if (log.action == discord.AuditLogAction.message_delete):
		if (log.user == msg.author):
			print("User deleted their own message; this will not be logged.")
		else:
			message = "{} deleted {}'s post in #{}: \n'{}'".format(log.user.mention, msg.author.mention, msg.channel.name, msg.content)
			print(message)
			await client.get_channel(channelid).send(message)

client.run(argv[2])
