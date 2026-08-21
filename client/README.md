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

From inside your Archipelago install (this client imports from the
Archipelago repo it's part of - it isn't standalone):

```
python JediAcademySPClient.py
```

Auto-detects the OpenJK homepath (tries the OneDrive-redirected Documents
path first, then the plain one). If neither exists yet, start the game once
first so it gets created, or check `find_openjk_homepath()` in the client
if your setup is different.

If items don't seem to be applying after a level load (they should
auto-resync, but just in case), the client has a manual `/resync` command.
