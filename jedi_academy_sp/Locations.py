from typing import Dict
from BaseClasses import Location
from .Data import BASE_ID, MISSIONS, objective_ids_for

# Locations start after the item ID range so the two never collide - not
# required by AP (items and locations are separate ID spaces per-world) but
# keeps debugging saner when both show up in the same log.
LOCATION_BASE_ID = BASE_ID + 10_000


class JALocation(Location):
	game = "Jedi Academy SP"


location_table: Dict[str, int] = {}
_next_id = LOCATION_BASE_ID

# Mission completion - fires from target_level_change_use in g_target.cpp
# when a tier mission's exit trigger fires, ID is "mission_complete_<map>"
# in the check-reached log line. One per tier mission.
MISSION_COMPLETE_LOCATIONS = {}  # mapname -> location name
for mapname, info in MISSIONS.items():
	name = f"{info['display']}: Mission Complete"
	MISSION_COMPLETE_LOCATIONS[mapname] = name
	location_table[name] = _next_id
	_next_id += 1

# Objectives - fires from Q3_SetObjective in Q3_Interface.cpp on
# SET_OBJ_SUCCEEDED, ID is the objective's own enum name (e.g.
# "T1_DANGER_OBJ1") straight from objectives.h, already globally unique.
OBJECTIVE_LOCATIONS = {}  # mapname -> {obj_enum: location name}
for mapname, info in MISSIONS.items():
	OBJECTIVE_LOCATIONS[mapname] = {}
	for i, obj_enum in enumerate(objective_ids_for(mapname), start=1):
		name = f"{info['display']}: Objective {i}"
		OBJECTIVE_LOCATIONS[mapname][obj_enum] = name
		location_table[name] = _next_id
		_next_id += 1

# NOTE: secrets (target_secret_use in g_target.cpp, ID scheme
# "secret_<map>_<x>_<y>_<z>") are NOT included yet - that needs extracting
# target_secret entities from the compiled .bsp files first (same approach
# as the RTCW project's build_treasure_document_tracker.py), which hasn't
# been done. The C++ hook already exists and logs correctly; this world just
# doesn't know the location IDs to register yet. Add a SECRET_LOCATIONS dict
# here once that extraction is done, matching the same pattern above.

location_name_to_id: Dict[str, int] = dict(location_table)

# Reverse lookup used by the client to map a check-reached log ID straight to
# an AP location name without re-deriving the naming scheme.
CHECK_ID_TO_LOCATION_NAME: Dict[str, str] = {}
for mapname, loc_name in MISSION_COMPLETE_LOCATIONS.items():
	CHECK_ID_TO_LOCATION_NAME[f"mission_complete_{mapname}"] = loc_name
for mapname, obj_map in OBJECTIVE_LOCATIONS.items():
	for obj_enum, loc_name in obj_map.items():
		CHECK_ID_TO_LOCATION_NAME[obj_enum] = loc_name
