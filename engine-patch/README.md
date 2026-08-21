# Engine Patch

A patch against [JACoders/OpenJK](https://github.com/JACoders/OpenJK) (the
actively-maintained open-source reimplementation of the Jedi Academy/Jedi
Outcast engine, GPLv2, built from Raven's original source release) adding
Archipelago check/lock hooks to the SP game logic. This is a source patch
against the real game code, not a memory hack or a runtime hook - the same
approach taken for the Return to Castle Wolfenstein AP integration this
world's author also worked on.

## What it does

- **Mission-tier locks**: the 14 non-linear holomap missions are gated
  behind `g_apUnlock_<mapname>` cvars, enforced at the single choke point
  every map load passes through (`SV_Map_()` in `code/server/sv_ccmds.cpp`),
  not just a UI-side grey-out.
- **Weapon locks**: all 15 weapons (including the saber) gated behind
  `g_apUnlock_weapon_<classname>` cvars, both at the item-pickup level
  (`Pickup_Weapon` in `code/game/g_items.cpp`) and the spawn-time default
  grant (`code/game/g_client.cpp`) that vanilla otherwise uses to hand you a
  saber on every fresh level spawn regardless of pickups.
- **Force powers**: the vanilla post-mission skill-point spend is
  suppressed (checks, not locks - the event is detected and reported, but
  doesn't apply the vanilla effect), starting levels are stripped to 0
  (including the two levels vanilla granted for free), and 16 new
  `ap_setForce<X>`/`ap_setSaber<X>` commands let an external client set any
  power to any level directly, without needing `sv_cheats`.
- **Checks**: objectives, secrets, and mission completion are all detected
  and logged (`Archipelago: ... check reached (...)`) as they happen during
  normal play, without being gated at all.
- **Client communication**: this SP build has no rcon at all. Reading
  checks needs no code (the engine's built-in `logfile` cvar already mirrors
  every console print to `qconsole.log`); sending commands in uses a new
  poll loop (`AP_PollCommandQueue()` in `code/game/g_main.cpp`) that reads
  and executes `ap_commands.txt` twice a second, then clears it.

## Building

1. Clone OpenJK: `git clone https://github.com/JACoders/OpenJK.git`
2. Apply `ja-sp-src.patch` from this directory: `git apply
   /path/to/ja-sp-src.patch` (run from the OpenJK repo root).
3. Requires CMake and a MSVC toolchain (VS2022 Build Tools with the C++
   workload, or Community/Professional). From the repo root:
   ```
   mkdir build && cd build
   cmake -G "Visual Studio 17 2022" -A Win32 -D CMAKE_INSTALL_PREFIX=../install ..
   cmake --build . --config Release
   ```
4. Deploy `openjk_sp.x86.exe` into your Jedi Academy `GameData/` folder,
   and `jagamex86.dll` specifically into `GameData/base/` (not the
   `GameData/` root - the game-logic DLL has a stricter search path than
   the engine exe itself, which will run fine from either location).

## Base commit

Patch was generated against OpenJK commit `1a6a643427aa347553e9073dac5570b33337c4d9`.
