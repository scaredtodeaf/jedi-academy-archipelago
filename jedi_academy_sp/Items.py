from typing import Dict, NamedTuple
from BaseClasses import Item, ItemClassification
from .Data import BASE_ID, MISSIONS, WEAPONS, FORCE_POWERS


class JAItem(Item):
	game = "Jedi Academy SP"


class JAItemData(NamedTuple):
	code: int
	classification: ItemClassification


item_table: Dict[str, JAItemData] = {}
_next_id = BASE_ID

# Reverse lookups the client uses to turn a received item name into the
# actual in-game console command. Non-progressive items map straight to a
# one-shot command string; progressive force items are handled separately
# below (client needs to track how many copies of each it's received so far
# to know what level to set, since ap_setForce<X> is an absolute set, not an
# increment - see Svcmd_ForceSetLevel_f in g_svcmds.cpp).
ITEM_TO_GAME_COMMAND: Dict[str, str] = {}

# Mission access - one per tier mission, gates g_apUnlock_<mapname>.
# All progression: each one is required to reach that mission's locations.
for mapname, info in MISSIONS.items():
	name = f"Access: {info['display']}"
	item_table[name] = JAItemData(_next_id, ItemClassification.progression)
	ITEM_TO_GAME_COMMAND[name] = f"set g_apUnlock_{mapname} 1"
	_next_id += 1

# Weapon unlocks - gates g_apUnlock_weapon_<classname> (see Pickup_Weapon in
# g_items.cpp and the spawn-time grant fix in g_client.cpp). The saber is
# progression (functionally required - confirmed live, you cannot fight
# through a tier mission without it). The rest are marked useful rather than
# progression - real alternate loadouts exist (force-only play is slow but
# possible), so they don't strictly gate access to anything.
for classname, display in WEAPONS.items():
	name = f"Weapon: {display}"
	classification = (ItemClassification.progression if classname == "weapon_saber"
					   else ItemClassification.useful)
	item_table[name] = JAItemData(_next_id, classification)
	ITEM_TO_GAME_COMMAND[name] = f"set g_apUnlock_{classname} 1"
	_next_id += 1

# Progressive force powers - one item per level per power (e.g. "Progressive
# Force Jump" appears 3 times in the pool; receiving copy N sets that power
# to level N via ap_setForce<X>/ap_setSaber<X>, see Svcmd_ForceSetLevel_f in
# g_svcmds.cpp). All progression - Force Jump in particular is confirmed
# live to gate real level traversal (t1_danger's last objective needs it).
PROGRESSIVE_FORCE_ITEM_NAMES = {}  # svcmd_suffix -> item name, used by Rules.py
PROGRESSIVE_ITEM_NAME_TO_SVCMD = {}  # item name -> svcmd_suffix, used by the client
for svcmd_suffix, display, max_level in FORCE_POWERS:
	name = f"Progressive {display}"
	PROGRESSIVE_FORCE_ITEM_NAMES[svcmd_suffix] = name
	PROGRESSIVE_ITEM_NAME_TO_SVCMD[name] = svcmd_suffix
	item_table[name] = JAItemData(_next_id, ItemClassification.progression)
	_next_id += 1

# Filler - pads the item pool to match the location count (see Locations.py;
# item count is short of location count once secrets are added, and even
# without them any generation-time rounding needs filler to fill leftover
# slots). No gameplay effect - flavor-only credit item, doesn't map to any
# ap_* command at all.
FILLER_ITEM_NAME = "Bacta Canister"
item_table[FILLER_ITEM_NAME] = JAItemData(_next_id, ItemClassification.filler)
_next_id += 1

item_name_to_id: Dict[str, int] = {name: data.code for name, data in item_table.items()}
