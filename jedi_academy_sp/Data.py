"""
Shared static data for the Jedi Academy SP world.

Everything here is derived from the ja-sp-src patch built in the same working
directory (D:\\Claude Stuff\\Archiplego modded one\\ja-sp-src) - map names,
objective counts, weapon classnames, and force power levels all come straight
from that source, not guesswork. Where a fact was only confirmed by live
testing rather than reading the source, it's called out in a comment.

Base ID: arbitrary, picked to be unlikely to collide with any other AP world
in a personal/private install. No significance beyond that.
"""

BASE_ID = 88_300_000

# ---------------------------------------------------------------------------
# Missions
# ---------------------------------------------------------------------------
# The 14 non-linear holomap missions, confirmed from the game's own
# levelshot/menu asset names. Prologue (yavin1/yavin1b/yavin2/t1_sour/
# t1_inter) and the fixed post-holomap endgame (hoth2/3, kor1/2, taspir1/2,
# vjun1-3) are linear, un-randomized vanilla progression - not represented
# here at all, same scope as the lock/check code in ja-sp-src.
#
# objective_count is read directly from objectives.h's enum block for each
# mission (e.g. T1_DANGER_OBJ1..OBJ5 = 5). t2_rancor has an OBJ5_2 in
# addition to OBJ1-6, so its count is 7, not 6.
MISSIONS = {
	"t1_danger":   {"tier": 1, "display": "Danger Room",        "objective_count": 5},
	"t1_fatal":    {"tier": 1, "display": "Fatal Alliance",     "objective_count": 6},
	"t1_rail":     {"tier": 1, "display": "Rail Advance",       "objective_count": 3},
	"t1_surprise": {"tier": 1, "display": "Surprise",           "objective_count": 4},
	"t2_dpred":    {"tier": 2, "display": "Deadly Predicament", "objective_count": 4},
	"t2_rancor":   {"tier": 2, "display": "Rancor Pit",         "objective_count": 7},
	"t2_rogue":    {"tier": 2, "display": "Rogue Shadows",      "objective_count": 2},
	"t2_trip":     {"tier": 2, "display": "Triple Threat",      "objective_count": 2},
	"t2_wedge":    {"tier": 2, "display": "Wedge's Rescue",     "objective_count": 12},
	"t3_bounty":   {"tier": 3, "display": "Bounty Hunt",        "objective_count": 9},
	"t3_byss":     {"tier": 3, "display": "Byss",               "objective_count": 3},
	"t3_hevil":    {"tier": 3, "display": "Heart of Evil",      "objective_count": 3},
	"t3_rift":     {"tier": 3, "display": "The Rift",           "objective_count": 3},
	"t3_stamp":    {"tier": 3, "display": "Stamp Out",          "objective_count": 4},
}

MISSION_MAPNAMES = list(MISSIONS.keys())

# Objective enum names actually used in objectives.h - built here so
# Locations.py doesn't have to hand-count. T2_RANCOR's extra OBJ5_2 is
# handled as its own explicit entry since it doesn't fit the OBJ<n> pattern.
def objective_ids_for(mapname: str):
	count = MISSIONS[mapname]["objective_count"]
	prefix = mapname.upper()
	if mapname == "t2_rancor":
		return [f"{prefix}_OBJ1", f"{prefix}_OBJ2", f"{prefix}_OBJ3", f"{prefix}_OBJ4",
				f"{prefix}_OBJ5", f"{prefix}_OBJ5_2", f"{prefix}_OBJ6"]
	return [f"{prefix}_OBJ{i}" for i in range(1, count + 1)]

# ---------------------------------------------------------------------------
# Weapons
# ---------------------------------------------------------------------------
# classname is exactly the QUAKED entity classname from bg_misc.cpp, which is
# also exactly what g_apUnlock_weapon_<classname> expects in g_items.cpp /
# g_client.cpp.
WEAPONS = {
	"weapon_saber":             "Lightsaber",
	"weapon_stun_baton":        "Stun Baton",
	"weapon_bryar_pistol":      "Bryar Pistol",
	"weapon_blaster_pistol":    "Blaster Pistol",
	"weapon_blaster":           "Blaster Rifle",
	"weapon_disruptor":         "Disruptor Rifle",
	"weapon_bowcaster":         "Bowcaster",
	"weapon_repeater":          "Golan Arms Flechette",  # classname is weapon_repeater in-engine
	"weapon_demp2":             "DEMP2",
	"weapon_flechette":         "Golan Arms Flechette Launcher",
	"weapon_concussion_rifle":  "Concussion Rifle",
	"weapon_rocket_launcher":   "Merr-Sonn PLX-2M Rocket Launcher",
	"weapon_thermal":           "Thermal Detonator",
	"weapon_trip_mine":         "Trip Mine",
	"weapon_det_pack":          "Detonation Pack",
}

# ---------------------------------------------------------------------------
# Force powers
# ---------------------------------------------------------------------------
# (svcmd suffix used by ap_setForce<X> / ap_setSaber<X>, display name, max level)
# Max levels read directly from SetForceTable in g_svcmds.cpp. Everything is
# FORCE_LEVEL_3 (i.e. 3) except Mind Trick, which is FORCE_LEVEL_4.
FORCE_POWERS = [
	("ForceHeal",       "Force Heal",        3),
	("ForceJump",       "Force Jump",        3),
	("ForceSpeed",      "Force Speed",       3),
	("ForcePush",       "Force Push",        3),
	("ForcePull",       "Force Pull",        3),
	("MindTrick",       "Mind Trick",        4),
	("ForceGrip",       "Force Grip",        3),
	("ForceLightning",  "Force Lightning",   3),
	("SaberThrow",      "Saber Throw",       3),
	("SaberDefense",    "Saber Defense",     3),
	("SaberOffense",    "Saber Offense",     3),
	("ForceRage",       "Force Rage",        3),
	("ForceProtect",    "Force Protect",     3),
	("ForceAbsorb",     "Force Absorb",      3),
	("ForceDrain",      "Force Drain",       3),
	("ForceSight",      "Force Sight",       3),
]
