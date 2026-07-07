import discord, stats, pathlib, json
from datetime import datetime, timedelta, timezone

BLACKLIST_FILE = "blacklist.json"
REPORT_FILE = "trustedreporters.json"
blacklist = {}
reporters = []

def load():
    global blacklist; global reporters
    assert(pathlib.Path(BLACKLIST_FILE).exists())
    with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
        blacklist = json.load(f)
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        reporters = json.load(f)

def save():
    with open(BLACKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(blacklist, f, indent=4)

load()

async def trap(message: discord.message.Message, allGuilds: list):
    member = message.author

    if blacklist.get(str(member.id)) == "warned" or (member.joined_at is not None and datetime.now(timezone.utc) - member.joined_at < timedelta(days=30)):
        await ban(message.author, f"Message in trap \"{message.content[:250]}\"", allGuilds)
    else:
        await mute(message.author, f"Message in trap \"{message.content[:250]}\"", allGuilds)

async def ban(user: discord.User, reason: str, allGuilds: list):
    for guild in allGuilds:
        for member in guild.members:
            if member.id == user.id:
                await member.ban(delete_message_days=1, reason=reason)
    blacklist[user.name] = "banned"
    save()
    stats.ban_on(user.guild.id)

async def mute(user: discord.User, reason: str, allGuilds: list):
    for guild in allGuilds:
        for member in guild.members:
            if member.id == user.id:
                await member.timeout(timedelta(days=10),reason=reason)
    blacklist[user.name] = "warned"
    save()
    stats.ban_on(user.guild.id)

def report(id: str, user: discord.User):
    if user.id not in reporters:
        return
    blacklist[id] = "report"
    save()
    stats.ban_on(user.guild.id)

async def member_join(member: discord.Member):
    match blacklist.get(member):
        case "banned":
            member.ban("Spambot was already catched")
            stats.ban_on(member.guild.id)
        case "warned":
            member.timeout(timedelta(days=10), "User was already catched in spam bot channel")
            stats.ban_on(member.guild.id)
        case "report":
            member.guild.system_channel.send(content=f"**Warning!** {member.mention} was reported as spammer.")