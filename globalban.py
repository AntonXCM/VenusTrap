import discord, stats, pathlib, json
from datetime import datetime, timedelta, timezone

BLACKLIST_FILE = "stats.json"
REPORT_FILE = "trustedreporters.json"
blacklist = {}
reporters = []
def Load():
    global blacklist; global reporters
    assert(pathlib.Path(BLACKLIST_FILE).exists())
    with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
        blacklist = json.load(f)
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        reporters = json.load(f)

def Save():
    with open(BLACKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(blacklist, f, indent=4)

Load()

async def Trap(message: discord.message.Message, allGuilds: list):
    member = message.author

    if blacklist.get(str(member.id)) == "warned" or (member.joined_at is not None and datetime.now(timezone.utc) - member.joined_at < timedelta(days=30)):
        await Ban(message.author, f"Message in trap \"{message.content[:250]}\"", allGuilds)
    else:
        await Mute(message.author, f"Message in trap \"{message.content[:250]}\"", allGuilds)

async def Ban(user: discord.User, reason: str, allGuilds: list):
    for guild in allGuilds:
        for member in guild.members:
            if member.id == user.id:
                await member.ban(delete_message_days=1, reason=reason)
    blacklist[user.name] = "banned"
    Save()
    stats.BanOn(user.guild.id)

async def Mute(user: discord.User, reason: str, allGuilds: list):
    for guild in allGuilds:
        for member in guild.members:
            if member.id == user.id:
                await member.timeout(timedelta(days=10),reason=reason)
    blacklist[user.name] = "warned"
    Save()
    stats.BanOn(user.guild.id)

def Report(id: str, user: discord.User):
    if user.id not in reporters:
        return
    blacklist[id] = "report"
    Save()
    stats.BanOn(user.guild.id)