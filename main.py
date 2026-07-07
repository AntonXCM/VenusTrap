import traps, globalban, discord, winsound, os, commands

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
    for guild in client.guilds:
        print("I'm on " + guild.name + " owned by " + guild.owner.global_name)

    print(f"Logged in as {client.user}")
    await commands.register_all(client)

@client.event
async def on_guild_join(guild: discord.Guild):
    winsound.Beep(1200, 300)
    print("I got added to " + guild.name)
    say_hi(guild)

async def say_hi(guild: discord.Guild):
    async def say_hi_in(channel: discord.TextChannel):
        await channel.send("Hewwo ewerywone!! I ám ***Venus***, ánd exíted tó bé hére! **:**3ɔ")
        await channel.send("My occupáton is spámbot défence! Run `/howdoidefend` tó gét PRO típs!")
        await channel.send("If you gót addítıonal quéstıons ásk my créator <@809036790416539658>")
    
    member = guild.get_member(client.user.id)
    if guild.system_channel != None and guild.system_channel.permissions_for(member).send_messages:
        await say_hi_in(guild.system_channel)
    else:
        for channel in guild.channels:
            if channel.permissions_for(member).send_messages and channel is discord.TextChannel:
                await say_hi_in(channel)
                return

@client.event
async def on_guild_remove(guild: discord.Guild):
    print("I got removed from "+ guild.name)
    for channel in guild.channels:
        traps.remove(channel.id)

@client.event
async def on_member_join(member: discord.Member):
    await globalban.member_join(member)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot or message.author.guild_permissions.administrator or message.author.id == 809036790416539658:
        return
    elif message.channel.id in traps.channels:
        try:
            await globalban.trap(message, client.guilds)
        except Exception as e:
            await message.reply(f"AAHH I CAN'T TRAP YOU. YOU'RE TOO STRONG {e}")

from dotenv import load_dotenv
load_dotenv()

client.run(os.environ["Token"])