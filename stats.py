import json, pathlib

STATS_FILE = "stats.json"

stats = {}

def load():
    global stats
    assert(pathlib.Path(STATS_FILE).exists())
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)

def save():
	with open(STATS_FILE, "w", encoding="utf-8") as f:
		json.dump(stats, f, indent=4, sort_keys=True)

def ban_on(guild_id):
    guild_id = str(guild_id)
    global stats
    if "guild_bans" not in stats:
        stats["guild_bans"] = {}
    guild_bans = stats["guild_bans"]
    if guild_id not in guild_bans:
        guild_bans[guild_id] = 0
    guild_bans[guild_id] += 1
    save()

def get_ban_stats_str(guilds: list) -> str:
    global stats
    guild_bans: dict = stats.get("guild_bans", {})
    lines = []
    longest_name = 9
    for _, name in guilds:
        longest_name = max(longest_name, len(name))
    lines.append("┌─"+"─" * longest_name + "─┬──────┐")
    lines.append("│ Server ID" + " "*(longest_name-9) +" │ Bans │")
    lines.append("├─"+"─" * longest_name + "─┼──────┤")

    for gid, name in guilds:
        lines.append(f"│ {_fix_line(name, longest_name)} │ {guild_bans.get(str(gid), 0):<4} │")

    lines.append("└─"+"─" * longest_name + "─┴──────┘")
    return "\n".join(lines)

def _fix_line(text, size):
	return text + " " * (size - len(text))

load()