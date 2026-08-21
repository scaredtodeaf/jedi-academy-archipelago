from worlds.generic.Rules import set_rule
from BaseClasses import MultiWorld
from .Data import MISSIONS
from .Items import PROGRESSIVE_FORCE_ITEM_NAMES


def set_rules(multiworld: MultiWorld, player: int):
	# Every mission needs its own access item, plus the lightsaber - confirmed
	# live this session that a tier mission is not practically completable
	# without a saber (see Weapon: Lightsaber's progression classification in
	# Items.py). The other 13 weapons stay optional/useful rather than being
	# hard requirements, since real alternate loadouts exist.
	for mapname, info in MISSIONS.items():
		entrance = multiworld.get_entrance(f"To {info['display']}", player)
		set_rule(entrance, lambda state, mapname=mapname, info=info: (
			state.has(f"Access: {info['display']}", player)
			and state.has("Weapon: Lightsaber", player)
		))

	# Known objective-level requirement, confirmed live this session:
	# t1_danger's final objective is unreachable without Force Jump 3 (there's
	# a gap in the level that needs it). Mapped to OBJ5 since t1_danger has 5
	# objectives and this was described as "the last one" - the exact
	# objective-to-in-level-order mapping hasn't been independently verified,
	# so treat this as a reasonable inference, not a confirmed fact, until
	# played through again to double check.
	#
	# No other objective->power/weapon requirements are encoded anywhere else
	# in this file - every other objective in every other mission is only
	# gated by its mission's own access rule above. This is very likely wrong
	# in some cases (some objectives almost certainly need specific weapons
	# or force powers to reach, the same way t1_danger's did) but nothing
	# else has actually been verified by play, and guessing at the rest would
	# risk generating unwinnable seeds in the opposite direction (requiring
	# items that aren't actually needed). Needs a real playthrough pass to
	# fill in properly.
	jump_location = multiworld.get_location("Danger Room: Objective 5", player)
	set_rule(jump_location, lambda state: state.has(
		PROGRESSIVE_FORCE_ITEM_NAMES["ForceJump"], player, 3))
