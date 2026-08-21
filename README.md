# Jedi Academy SP - Archipelago World

An [Archipelago](https://archipelago.gg/) multiworld randomizer integration
for **Star Wars Jedi Knight: Jedi Academy** (2003), Single Player campaign,
built on top of a source patch to
[OpenJK](https://github.com/JACoders/OpenJK) - the actively-maintained
open-source reimplementation of the game's engine (GPLv2, from Raven's
original source release), not a memory hack.

**Status: work in progress.** The world generates correctly and every
game-side mechanic has been verified live in-game, but it has not yet been
tested end-to-end in a real multiworld with other players. See
[`research/notes.md`](research/notes.md) for known limitations before
relying on this for anything but solo testing.

14 non-linear holomap missions, 15 weapons, and 16 force powers (49 levels
total) are all real Archipelago items. 81 locations across mission
completions and in-mission objectives. The prologue and the fixed
post-holomap endgame are intentionally left as vanilla, unrandomized
progression - see the world's setup guide for the full scope.

## What's in this repo

- **[`jedi_academy_sp/`](jedi_academy_sp/)** - the Archipelago world source
  (item/location tables, region graph, access rules).
- **`jedi_academy_sp.apworld`** - the packaged world file. Drop this into
  your Archipelago install's `custom_worlds` folder.
- **[`client/`](client/)** - the client you run alongside the game.
- **[`engine-patch/`](engine-patch/)** - the actual gameplay-side work: a
  patch against OpenJK adding the check/lock hooks this world needs, plus
  build instructions. Prefer not to build it yourself? Grab a
  [prebuilt Windows binary](../../releases/latest) instead - just drop it
  into your existing Jedi Academy install.
- **[`research/notes.md`](research/notes.md)** - facts and gotchas found
  along the way (map/objective/weapon/force-power data pulled straight from
  source, plus debugging gotchas worth not rediscovering).

## Setup

See [`jedi_academy_sp/docs/setup_en.md`](jedi_academy_sp/docs/setup_en.md)
for the full walkthrough (build the engine patch, install the world,
configure logging, run the client).

## License

The engine patch is against OpenJK, itself GPLv2. The world/client code
here follows Archipelago's own licensing conventions for custom worlds.
