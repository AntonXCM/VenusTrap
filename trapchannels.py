import pathlib, json, stats
TRAP_CHANNELS_FILE = "trap-channels.json"

trapChannels = []

def LoadTrapChannels():
	global trapChannels

	assert(pathlib.Path(TRAP_CHANNELS_FILE).exists())
	with open(TRAP_CHANNELS_FILE, "r", encoding="utf-8") as f:
		trapChannels = json.load(f)

def SaveTrapChannels():
	with open(TRAP_CHANNELS_FILE, "w", encoding="utf-8") as f:
		json.dump(trapChannels, f, indent=4)

def add(trap) -> bool:
	if trap not in trapChannels:
		trapChannels.append(trap)
		SaveTrapChannels()
		return True
	return False

def remove(trap) -> bool:
	if trap in trapChannels:
		trapChannels.remove(trap)
		SaveTrapChannels()
		return True
	return False

LoadTrapChannels()