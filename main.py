# Settings
TOKEN = "MTUxNjIzOTkyMjE1MzkxODYxNQ.GsEy4Q.iMhXvSdbA1we1zrG9d9M7txQfX3vPCdNaTDgiM"

import trapchannels, stats, globalban, discord, winsound

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
            if trapchannels.Add(message.channel.id):
                await message.reply("The channel is a trap\n# DON'T WRITE ANYTHING IN HERE\n# IT WILL BAN YOU PERMANENTLY IN EVERY SERVER\n# WHERE VENUS HONEYPOT IS LOCATED")
        
        elif message.content.startswith("!removetrap"):
            if trapchannels.Remove(message.channel.id):
                await message.reply("The channel is no longer a trap")

        elif message.content.startswith("!banstats"):
            if message.content.endswith("all"):
                await message.reply(stats.GetBanStats([(guild.id, guild.name) for guild in client.guilds]))
            else:
                await message.reply(f"On server {message.guild.name} was banned {stats.stats.get("guild_bans", {}).get(message.guild.id, 0)} bots")
        
        elif message.content.startswith("!report "):
            if message.author.id not in globalban.reporters:
                await message.reply("You're not trusted to report")
                return
            
            reports = message.content.split(" ")
            reports.remove("!report")
            for report in reports:
                globalban.Report(report, message.author)
            await message.reply("Thank you for reporting!")
        
        elif message.content.startswith("!allbans"):
            for name, status in globalban.blacklist.values:
                await message.reply(f"- {str(name)} is {status}")
    elif message.channel.id in trapchannels.trapChannels:
        try:
            await globalban.Trap(message, client.guilds)
        except Exception as e:
            await message.reply(f"Error attempting to trap {e}")

client.run(TOKEN)