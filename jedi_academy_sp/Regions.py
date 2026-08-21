from BaseClasses import Region, Entrance
from .Data import MISSIONS
from .Locations import JALocation, MISSION_COMPLETE_LOCATIONS, OBJECTIVE_LOCATIONS, location_table


def create_regions(world):
	player = world.player
	multiworld = world.multiworld

	menu = Region("Menu", player, multiworld)
	multiworld.regions.append(menu)

	# Flat structure - each tier mission is its own region reachable directly
	# from Menu (no mission requires having beaten another mission first,
	# matching the real holomap: all 14 are independently selectable once
	# unlocked). Objectives and the mission-complete location both live in
	# that mission's region.
	for mapname, info in MISSIONS.items():
		region = Region(info["display"], player, multiworld)

		complete_name = MISSION_COMPLETE_LOCATIONS[mapname]
		region.locations.append(
			JALocation(player, complete_name, location_table[complete_name], region))

		for obj_enum, loc_name in OBJECTIVE_LOCATIONS[mapname].items():
			region.locations.append(
				JALocation(player, loc_name, location_table[loc_name], region))

		multiworld.regions.append(region)

		entrance = Entrance(player, f"To {info['display']}", menu)
		menu.exits.append(entrance)
		entrance.connect(region)
