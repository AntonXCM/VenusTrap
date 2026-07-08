import discord, traps, stats, globalban, translaions
from discord import app_commands

client: discord.Client

@app_commands.default_permissions(administrator=True)
async def addtrap(interaction: discord.Interaction):
    if traps.add(interaction.channel_id):
        await interaction.response.send_message(translaions.tr("trap", interaction.guild_locale))

@app_commands.default_permissions(administrator=True)
async def removetrap(interaction: discord.Interaction):
    if traps.remove(interaction.channel_id):
        await interaction.response.send_message(translaions.tr("untrap", interaction.guild_locale))

async def banstats(interaction: discord.Interaction, all: bool = False):
    if all:
        global client
        await interaction.response.send_message(
            translaions.tr("chart1", interaction.locale) + '\n```' +
            stats.get_ban_stats_str([(guild.id, guild.name) for guild in client.guilds]) +
            '```\n' + translaions.tr("chart2", interaction.locale),
            ephemeral=True)
    else:
        await interaction.response.send_message(translaions.tr("stats1", interaction.locale) + f" {stats.stats.get("guild_bans", {}).get(str(interaction.guild_id), 0)} " + translaions.tr("stats2", interaction.locale), ephemeral=True)

async def banlist(interaction: discord.Interaction):
    channel = interaction.channel
    for name, status in globalban.blacklist.values:
        await channel.send(f"- {str(name)} is {status}")

@app_commands.describe(username="User to report")
@app_commands.default_permissions(administrator=True)
async def report(interaction: discord.Interaction, username: str):
    if interaction.user.id not in globalban.reporters:
        await interaction.response.send_message(translaions.tr("reportfail", interaction.locale), ephemeral=True)
        return
    
    globalban.report(username, interaction.user)
    await interaction.response.send_message(translaions.tr("reportsucc", interaction.locale), ephemeral=True)

async def howdoidefend(interaction: discord.Interaction):
    await interaction.response.send_message(":thinking:", ephemeral=True)
    await interaction.channel.send(translaions.tr("guide1", interaction.locale))

    await interaction.channel.send(translaions.tr("guide2", interaction.locale))

    secondline = translaions.tr("guide3", interaction.locale)
    users = 1.0 / interaction.guild.member_count
    for role in interaction.guild.roles:
        if role.name == "@everyone":
            continue
        if len(role.members) * users >= 0.25 and role.mentionable:
            secondline += f" **\\@{role.name}**,"
    secondline += translaions.tr("guide4", interaction.locale)
    await interaction.channel.send(secondline)

    await interaction.channel.send(translaions.tr("guide5", interaction.locale))

async def fakeban(interaction: discord.Interaction):
    stats.ban_on(interaction.guild_id)

commands = {
    "addtrap": addtrap,
    "removetrap": removetrap,
    "banstats": banstats,
    "banlist": banlist,
    "report": report,
    "howdoidefend": howdoidefend
    }

async def register_all(p_client: discord.Client):
    global client
    client = p_client
    print("e")
    tree = app_commands.CommandTree(client)
    for i in commands:
        command = app_commands.Command(name=i, description='/'+i, callback = commands[i])
        tree.add_command(command)
    await tree.set_translator(translaions.Translator())
    await tree.sync()