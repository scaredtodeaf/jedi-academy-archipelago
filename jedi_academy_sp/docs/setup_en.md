# Jedi Academy SP Setup Guide

## Status

**Work in progress, not yet tested in a real multiworld with other
players.** The world generates correctly (verified with Archipelago's own
test suite and a real `Generate.py` run) and every game-side mechanic
(mission locks, weapon locks, force power items, check detection) has been
verified live in-game, but the client has not yet been run end-to-end
against a live server + the running game simultaneously. Expect rough
edges.

## Required Software

- [Star Wars Jedi Knight: Jedi Academy](https://store.steampowered.com/app/6020/)
  (Steam), installed normally.
- A build of the patched engine - see [`../../engine-patch/README.md`](../../engine-patch/README.md)
  for how to build it from the included patch. There's no pre-built binary
  in this repo (the patch applies to [JACoders/OpenJK](https://github.com/JACoders/OpenJK),
  a separate GPL-licensed codebase not vendored here).
- Python 3.10+ and a working Archipelago install (this world isn't
  self-contained - the client imports from the Archipelago repo it's
  dropped into).

## Installation

1. Build the patched engine per `engine-patch/README.md` and deploy it into
   your Jedi Academy `GameData/base/` folder (the game DLL specifically
   needs to go in `base/`, not the `GameData/` root - the engine exe itself
   works from either).
2. Add `seta logfile "2"` to your `openjk_sp.cfg` (usually
   `<Documents>/My Games/OpenJK/base/openjk_sp.cfg`) so the engine mirrors
   console output to `qconsole.log`, which the client reads.
3. Drop `jedi_academy_sp.apworld` into your Archipelago install's
   `custom_worlds` folder.
4. Generate a game normally (`Generate.py`, or the Archipelago Launcher),
   including a player YAML with `game: Jedi Academy SP`.

## Playing

1. Launch the patched game and start a new campaign (or load an existing
   AP save).
2. Run `client/JediAcademySPClient.py` from inside your Archipelago
   install, and connect it to your server the normal way.
3. Play through the prologue (Yavin training) normally - it's intentionally
   unrandomized vanilla content. Once you reach the holomap, every mission,
   weapon, and force power level is a real Archipelago item somewhere in
   the multiworld.

## Known Limitations

- Secrets aren't check locations yet - the in-game hook exists and logs
  correctly, but the world doesn't know the location IDs (needs extracting
  `target_secret` entities from the compiled `.bsp` files first).
- Only one specific objective->item requirement has been verified by real
  play (Danger Room's last objective needs 3 levels of Force Jump). Every
  other objective is only gated by its mission's own access item - some are
  almost certainly reachable-in-theory-but-not-in-practice without specific
  weapons or force powers, the same way that one was, but nothing else has
  been confirmed by an actual playthrough.
- No support yet for saving/loading mid-mission with AP item state
  preserved beyond what the client's resync-on-level-load handles.
