import pathlib, json, stats
TRAP_CHANNELS_FILE = "trap-channels.json"

trapChannels = []

def Load():
	global trapChannels
	assert(pathlib.Path(TRAP_CHANNELS_FILE).exists())
	with open(TRAP_CHANNELS_FILE, "r", encoding="utf-8") as f:
		trapChannels = json.load(f)

def Save():
	with open(TRAP_CHANNELS_FILE, "w", encoding="utf-8") as f:
		json.dump(trapChannels, f, indent=4)

def Add(trap) -> bool:
	if trap not in trapChannels:
		trapChannels.append(trap)
		Save()
		return True
	return False

def Remove(trap) -> bool:
	if trap in trapChannels:
		trapChannels.remove(trap)
		Save()
		return True
	return False

Load()