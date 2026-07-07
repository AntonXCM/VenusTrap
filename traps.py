import pathlib, json, stats
TRAP_CHANNELS_FILE = "trap-channels.json"

channels = []

def load():
	global channels
	assert(pathlib.Path(TRAP_CHANNELS_FILE).exists())
	with open(TRAP_CHANNELS_FILE, "r", encoding="utf-8") as f:
		channels = json.load(f)

def save():
	with open(TRAP_CHANNELS_FILE, "w", encoding="utf-8") as f:
		json.dump(channels, f, indent=4)

def add(trap: int) -> bool:
	if trap not in channels:
		channels.append(trap)
		save()
		return True
	return False

def remove(trap: int) -> bool:
	if trap in channels:
		channels.remove(trap)
		save()
		return True
	return False

load()