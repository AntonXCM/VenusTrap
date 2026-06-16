# Settings
TOKEN = "MTUxNjIzOTkyMjE1MzkxODYxNQ.GsEy4Q.iMhXvSdbA1we1zrG9d9M7txQfX3vPCdNaTDgiM"

from datetime import datetime, timedelta, timezone
import trapchannels, stats, discord, winsound

intents = discord.Intents.none()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.bans = True
intents.moderation = True
intents.typing = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_guild_join(guild: discord.Guild):
    winsound.Beep(1200, 300)
    print(guild)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.author.guild_permissions.administrator:
        if message.content.startswith("!addtrap"):
            if trapchannels.add(message.channel.id):
                await message.reply("The channel is a trap\n# DON'T WRITE ANYTHING IN HERE\n# IT WILL BAN YOU PERMANENTLY IN EVERY SERVER\n# WHERE VENUS HONEYPOT IS LOCATED")
        elif message.content.startswith("!removetrap"):
            if trapchannels.remove(message.channel.id):
                await message.reply("The channel is no longer a trap")
        elif message.content.startswith("!banstats"):
            if message.content.endswith("all"):
                await message.reply(stats.GetBanStats([(guild.id, guild.name) for guild in client.guilds]))
            else:
                await message.reply(f"On server {message.guild.name} was banned {stats.stats.get("guild_bans", {}).get(message.guild.id, 0)} bots")
    else:
        if message.channel.id in trapchannels.trapChannels:
            await trap(message)

async def trap(message: discord.message.Message):
    member = message.author

    if member.joined_at is None or datetime.now(timezone.utc) - member.joined_at > timedelta(days=30):
        return
    print(str(message.guild.self_role.permissions))
    try:
        await member.ban(reason=f"Message in trap \"{message.content[:250]}\"")
        stats.BanOn(message.guild.id)
    except Exception as e:
        await message.reply(e)


client.run(TOKEN)