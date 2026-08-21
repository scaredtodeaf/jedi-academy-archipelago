# Jedi Academy SP Client

Connects a running (patched) Jedi Academy SP session to an Archipelago
multiworld. Entirely file-based - no rcon, no memory reading, no mod-side
network code:

- **Checks**: tails `qconsole.log` (needs `logfile 2` set - see the setup
  guide) for `Archipelago: ... check reached (...)` lines and reports them
  to the server as they happen.
- **Items**: on every item received, rewrites `ap_commands.txt` from
  scratch with the console command for everything received so far (mission
  unlocks, weapon unlocks, force power levels). The patched engine polls
  and executes that file twice a second, then clears it.
- **Resync**: force power levels reset to 0 on every fresh level load
  (confirmed live - the game's `ClientSpawn` wipes the player state struct
  on respawn), and loading a save restores whatever was true *at save
  time*, which can predate an item being received. So the client watches
  for `Server: <mapname>` lines in the log and re-sends every received
  item's command whenever it sees a new one, not just once when the item
  first arrives.

## Running

**Needs a source checkout of Archipelago, not a frozen/installed one.**
This client imports `Utils`, `CommonClient`, etc. from the Archipelago repo
it's dropped into - in a normal installed copy (the kind with
`Archipelago*.exe` files, like what the Archipelago website's installer
gives you), those modules only exist bundled inside the compiled exes, not
as loose importable `.py` files, so `python JediAcademySPClient.py` fails
with `ModuleNotFoundError: No module named 'Utils'` there. Clone
[ArchipelagoMW/Archipelago](https://github.com/ArchipelagoMW/Archipelago)
yourself, drop this client and `jedi_academy_sp/` (from `../jedi_academy_sp/`
in this repo) into it, and run from there instead - the Options Creator,
Generate, and Server can still be your regular frozen install; only the
client needs the source checkout.

From inside that checkout:

```
python JediAcademySPClient.py --connect host:port --name YourSlotName
```

`--password` too if the room needs one. `start_client.bat` in this folder
prompts for all of these interactively instead - edit the
`AP_SOURCE_CHECKOUT` path near the top of it to point at your own checkout
first.

Auto-detects the OpenJK homepath (tries the OneDrive-redirected Documents
path first, then the plain one). If neither exists yet, start the game once
first so it gets created, or check `find_openjk_homepath()` in the client
if your setup is different.

If items don't seem to be applying after a level load (they should
auto-resync, but just in case), the client has a manual `/resync` command.
