from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import JAItem, item_table, item_name_to_id, FILLER_ITEM_NAME, PROGRESSIVE_FORCE_ITEM_NAMES
from .Data import FORCE_POWERS
from .Locations import JALocation, location_name_to_id
from .Regions import create_regions
from .Rules import set_rules
from .Data import MISSIONS
from .Options import JediAcademySPOptions

client_version = 1


class JediAcademySPWeb(WebWorld):
	tutorials = [Tutorial(
		"Multiworld Setup Guide",
		"A guide to playing Star Wars Jedi Knight: Jedi Academy (SP) with Archipelago.",
		"English",
		"setup_en.md",
		"setup/en",
		["kelt"],
	)]


class JediAcademySPWorld(World):
	"""
	Star Wars Jedi Knight: Jedi Academy - Single Player.
	Play through the 14 non-linear holomap missions with your saber, weapons,
	and force powers scattered across the multiworld. Built on top of a
	source patch to OpenJK (the open-source engine/game reimplementation),
	not a memory hack.
	"""
	game = "Jedi Academy SP"
	options_dataclass = JediAcademySPOptions
	web = JediAcademySPWeb()

	item_name_to_id = item_name_to_id
	location_name_to_id = location_name_to_id

	def generate_early(self):
		# AP requires at least one location reachable with zero items (see
		# test/general/test_reachability.py's test_default_empty_state_can_
		# reach_something - caught this exact problem, every location here
		# was gated behind at least one Access item with nothing free).
		# Precollecting one starting mission plus the saber gives a real
		# foothold, and matches the actual game handing you a saber before
		# the holomap even opens. t1_danger is an arbitrary pick among the
		# four tier-1 missions - no in-game reason to prefer it over the
		# other three, just needed to pick one. Could become a player option
		# later; hard-coded for now, same staged-scope approach as
		# everything else in this world so far.
		starting_mission = MISSIONS["t1_danger"]["display"]
		self.multiworld.push_precollected(self.create_item(f"Access: {starting_mission}"))
		self.multiworld.push_precollected(self.create_item("Weapon: Lightsaber"))

	def create_regions(self):
		create_regions(self)

	def create_items(self):
		items_to_create = []
		progressive_names = set(PROGRESSIVE_FORCE_ITEM_NAMES.values())
		# These two were already handed out directly in generate_early() -
		# leave them out of the pool so there's exactly one copy of each
		# floating around total, not a redundant second one still to find.
		precollected_names = {f"Access: {MISSIONS['t1_danger']['display']}", "Weapon: Lightsaber"}
		for name, data in item_table.items():
			if name == FILLER_ITEM_NAME:
				continue
			if name in progressive_names:
				continue  # handled below - one copy per level, not per name
			if name in precollected_names:
				continue
			items_to_create.append(name)

		# Progressive force items need max_level copies each (e.g. 3 separate
		# "Progressive Force Jump" items in the pool, one per level) - missed
		# on the first pass, caught by test/general/test_reachability.py's
		# all-state check failing on "Danger Room: Objective 5" (the one
		# location that actually needs level 3, not just 1 copy).
		for svcmd_suffix, display, max_level in FORCE_POWERS:
			name = PROGRESSIVE_FORCE_ITEM_NAMES[svcmd_suffix]
			items_to_create += [name] * max_level

		# Pad with filler up to the location count - see Locations.py's
		# comment on why item count is short (secrets not extracted yet).
		location_count = len(location_name_to_id)
		while len(items_to_create) < location_count:
			items_to_create.append(FILLER_ITEM_NAME)

		self.multiworld.itempool += [self.create_item(name) for name in items_to_create]

	def create_item(self, name: str) -> JAItem:
		data = item_table[name]
		return JAItem(name, data.classification, data.code, self.player)

	def set_rules(self):
		set_rules(self.multiworld, self.player)
		# Logical completion = access to every mission. Whether the player
		# has actually *finished* the campaign in-game (all 14 missions
		# beaten) is tracked and reported by the client, not by this rule -
		# see ja_ap_client.py's goal-detection logic. This just guarantees a
		# generated seed is never logically unwinnable.
		self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
			[f"Access: {info['display']}" for info in MISSIONS.values()], self.player)

	def fill_slot_data(self):
		return {
			"client_version": client_version,
		}
