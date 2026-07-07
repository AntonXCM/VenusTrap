import discord, traps, stats, globalban
from discord import app_commands

client: discord.Client

@app_commands.default_permissions(administrator=True)
async def addtrap(interaction: discord.Interaction):
    if traps.add(interaction.channel_id):
        await interaction.response.send_message("The channel is a trap\n# DON'T WRITE ANYTHING IN HERE\n# IT WILL BAN YOU PERMANENTLY IN EVERY SERVER\n# WHERE VENUS HONEYPOT IS LOCATED")

@app_commands.default_permissions(administrator=True)
async def removetrap(interaction: discord.Interaction):
    if traps.remove(interaction.channel_id):
        await interaction.response.send_message("The channel is no longer a trap `{~v~}`")

async def banstats(interaction: discord.Interaction, all: bool = False):
    if all:
        global client
        await interaction.response.send_message(stats.get_ban_stats_str([(guild.id, guild.name) for guild in client.guilds]))
    else:
        await interaction.response.send_message("_JOOOOO_!!! `{XD}` I háve bánned" + f"{stats.stats.get("guild_bans", {}).get(str(interaction.guild_id), 0)} spámmers ín hére")

async def banlist(interaction: discord.Interaction):
    channel = interaction.channel
    for name, status in globalban.blacklist.values:
        await channel.send(f"- {str(name)} is {status}")

@app_commands.describe(username="User to report")
@app_commands.default_permissions(administrator=True)
async def report(interaction: discord.Interaction, username: str):
    if interaction.user.id not in globalban.reporters:
        await interaction.response.send_message("Yóu\\`re nót trústed tó réport, sory `{^ŵ}🗯`")
        return
    
    globalban.report(username, interaction.user)
    await interaction.response.send_message("**OK!** I wíll rémember hím :writing_hand:`{^^J}`")

async def howdoidefend(interaction: discord.Interaction):
    await interaction.response.send_message(":thinking:")
    await interaction.channel.send("**Hí!** Its me, ***Venus*** `{^v^⌯}`\n# Thís ís a _advíce líst_ hów dó you maxımíze your défence")

    await interaction.channel.send("**𝐅𝐢\U00000301𝐫𝐬𝐭**, máke a __públıc__ chánnel whére __ányone__ cán týpe!\n**Thén**, `/addtrap` tó thát chánnel!")

    secondline = "**𝐒𝐞\U00000301𝐜𝐨𝐧𝐭**, restríct píngıng **\\@éveryone** ánd róles móst péople hás, fór exámple"
    users = 1.0 / interaction.guild.member_count
    for role in interaction.guild.roles:
        if role.name == "@everyone":
            continue
        if len(role.members) * users >= 0.25:
            secondline += f" **\\@{role.name}**,"
    secondline += "ánd **\\@Venus Trap**.\n thén spámmers cóuld nót píng péople."
    await interaction.channel.send(secondline)

    await interaction.channel.send("**𝐓𝐡𝐢\U00000301𝐫𝐬𝐭**, `/réport` spámmers. Thén Ì\\`ll knów théy áre dangeróus `{◕‿◕}`")

commands = {
    "addtrap": addtrap,
    "removetrap": removetrap,
    "banstats": banstats,
    "banlist": banlist,
    "report": report,
    "howdoidefend": howdoidefend
    }

descriptions = {
    "addtrap": "Make channel to trap",
    "removetrap": "Untrap this channel",
    "banstats": "Show ban stats",
    "banlist": "Show all banned users",
    "report": "Report to a user",
    "howdoidefend": "Explains how to make your server safer!"
}

async def register_all(p_client: discord.Client):
    global client
    client = p_client
    print("e")
    tree = app_commands.CommandTree(client)
    for i in commands:
        command = app_commands.Command(name=i, description=descriptions.get(i), callback = commands[i])
        tree.add_command(command)
    await tree.sync()