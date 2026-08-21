# Research Notes

Facts and gotchas discovered while building this, kept here so they don't
have to be rediscovered. Everything below was confirmed either by reading
the OpenJK source directly or by live testing - noted which, since the two
carry different confidence levels.

## Mission structure (confirmed from source: pk3 asset names, objectives.h)

The real campaign opens on a linear prologue - `yavin1` -> `yavin1b` ->
`yavin2` -> `t1_sour` -> `t1_inter` - then opens onto a non-linear 3-tier
holomap:

- Tier 1: `t1_danger` (5 objectives), `t1_fatal` (6), `t1_rail` (3),
  `t1_surprise` (4)
- Tier 2: `t2_dpred` (4), `t2_rancor` (7 - has an `OBJ5_2` in addition to
  `OBJ1-6`), `t2_rogue` (2), `t2_trip` (2), `t2_wedge` (12)
- Tier 3: `t3_bounty` (9), `t3_byss` (3), `t3_hevil` (3), `t3_rift` (3),
  `t3_stamp` (4)

After all three tiers, a fixed linear endgame: `hoth2/3`, `kor1/2`,
`taspir1/2`, `vjun1-3`. None of the prologue/endgame is randomized - only
the 14 tier missions.

`academy1-6` exist as map files but never appear in `objectives.h`'s
objective table at all - they're not part of the real campaign flow,
despite being a very plausible guess for "the tutorial" (that guess was
wrong and cost real debugging time before the actual `Server: <mapname>`
log line settled it).

## Force powers (confirmed from source: `SetForceTable` in `g_svcmds.cpp`)

16 powers, all max level 3 except Mind Trick (max 4): Force Heal, Force
Jump, Force Speed, Force Push, Force Pull, Mind Trick, Force Grip, Force
Lightning, Saber Throw, Saber Defense, Saber Offense, Force Rage, Force
Protect, Force Absorb, Force Drain, Force Sight.

Vanilla's real (non-cheat) starting state was just Saber Offense/Defense at
level 1 - everything else starts at 0 and is earned via the post-mission
skill-point menu (one point per mission, player's free choice). This
project suppresses that menu's effect entirely and strips the two free
starting levels too, so every single level of every power comes from AP
items.

## Weapons (confirmed from source: `QUAKED weapon_*` entity defs in `bg_misc.cpp`)

15 total: `weapon_stun_baton`, `weapon_saber`, `weapon_bryar_pistol`,
`weapon_blaster_pistol`, `weapon_blaster`, `weapon_disruptor`,
`weapon_bowcaster`, `weapon_repeater`, `weapon_demp2`, `weapon_flechette`,
`weapon_concussion_rifle`, `weapon_rocket_launcher`, `weapon_thermal`,
`weapon_trip_mine`, `weapon_det_pack`.

## Gotchas (confirmed live, cost real debugging time)

- **Deploy location matters and isn't obvious.** `jagamex86.dll` must go in
  `GameData/base/`, not `GameData/` root. The engine exe itself runs fine
  from root (different, simpler loader), so this is easy to get wrong and
  have everything *look* like it's working while none of the actual C++
  patches are active. This exact mistake happened for a good chunk of a
  session before a `Sys_LoadSPGameDll(...) failed: module could not be
  found` log line caught it.
- **`set <command_name> <value>` creates a real cvar that shadows the
  command of the same name.** If someone ever fat-fingers `set
  ap_setForceJump 2` instead of `ap_setForceJump 2`, every future call to
  that command silently does nothing (it just updates the now-existing
  cvar instead of running the command) - no error, no warning. Only fix is
  a full engine restart (the stray cvar isn't `CVAR_ARCHIVE`, so it doesn't
  survive one). This produced a long, confusing "the command isn't working"
  debugging session before being traced through the no-arg query form
  printing `Cvar ap_setForceJump = "3", default = "2"` instead of the
  command's own status message.
- **Force Jump needs level 3 specifically for wall-jumping** - a different,
  separate gate (`PM_CheckGrabWall` in `bg_pmove.cpp`) than the basic
  height-boost mechanic (`PM_ForceJumpingUp`, which only needs level 1+).
  Easy to conflate the two and misdiagnose which one a specific level
  obstacle actually needs.
- **Force Jump (and the basic vertical boost generally) is a hold-to-rise
  mechanic**, not an instant higher jump - you have to keep holding the
  jump key while ascending, tapping it looks identical to a normal jump
  even with a high level set.
- **`ModuleUpdate.update()` (called by `Generate.py` and most reference
  clients) does a blanket dependency check across every registered world**,
  not just the one you're using - expect to need every `worlds/*/
  requirements.txt` installed too, not just the top-level
  `requirements.txt`, to get a clean run. The client in this repo skips
  that call entirely rather than requiring it.
