"""
Archipelago client for Star Wars Jedi Knight: Jedi Academy (SP), built on top
of the ja-sp-src OpenJK patch in the same working directory
(D:\\Claude Stuff\\Archiplego modded one\\ja-sp-src).

Communication with the running game is entirely file-based, since this SP
engine build has no rcon at all (confirmed by searching the whole
code/server/ tree - see project memory) and no other IPC:

  - Reading checks: the engine's built-in `logfile 2` cvar mirrors every
    console print to qconsole.log in real time, including every
    "Archipelago: ... check reached (...)" line the C++ patch prints. This
    client tails that file.
  - Sending items: AP_PollCommandQueue() in g_main.cpp polls ap_commands.txt
    (same directory) twice a second and executes each line as a real console
    command via gi.SendConsoleCommand, then clears the file. This client
    writes to that file.

Both files live in OpenJK's fs_homepath, normally
"<Documents>/My Games/OpenJK/base/" - auto-detected below, checking the
OneDrive-redirected path first since that's what this machine actually uses,
then falling back to the plain, non-redirected Documents path for anyone
without OneDrive folder redirection.

State-reset caveat (confirmed live this session): force power levels reset
to 0 on every fresh level load (ClientSpawn memsets the client struct), and
there is no save/reload persistence for AP-granted state either - loading a
save restores whatever was true *at save time*, which can predate an item
being received. So this client re-sends every received item's command any
time it sees a new "Server: <mapname>" line in the log, not just once when
the item first arrives. Mission-access and weapon-unlock cvars don't
strictly need this (cvars aren't reset by ClientSpawn), but resending them
too is harmless (they're just idempotent cvar sets), so everything gets
resynced together for simplicity.
"""
from __future__ import annotations
import os
import re
import asyncio

# Deliberately not calling ModuleUpdate.update() here (unlike most reference
# clients) - it does a blanket dependency check across every world in the
# Archipelago install, not just this one, which means it fails on missing
# optional extras for completely unrelated games (factorio-rcon-py,
# dolphin-memory-engine, etc.) rather than anything this client actually
# needs. If you can run any other Archipelago client from this same
# install, this one's real dependencies (colorama, websockets, ...) are
# already satisfied.

import Utils

if __name__ == "__main__":
	Utils.init_logging("JediAcademySPClient", exception_logger="Client")

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
	CommonContext, server_loop

from worlds.jedi_academy_sp.Items import ITEM_TO_GAME_COMMAND, PROGRESSIVE_ITEM_NAME_TO_SVCMD
from worlds.jedi_academy_sp.Locations import CHECK_ID_TO_LOCATION_NAME, location_name_to_id
from worlds.jedi_academy_sp.Data import MISSIONS

CHECK_REACHED_RE = re.compile(r"check reached \(([^)]+)\)")
SERVER_MAP_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} Server: (\S+)")

MISSION_COMPLETE_COUNT = len(MISSIONS)


def find_openjk_homepath() -> str:
	candidates = [
		os.path.expandvars(r"%USERPROFILE%\OneDrive\Documents\My Games\OpenJK\base"),
		os.path.expandvars(r"%USERPROFILE%\Documents\My Games\OpenJK\base"),
	]
	for path in candidates:
		if os.path.isdir(path):
			return path
	# Neither exists yet (fresh install, game never launched) - default to
	# the non-redirected path and let the caller create it if needed.
	return candidates[1]


class JediAcademySPCommandProcessor(ClientCommandProcessor):
	def _cmd_resync(self):
		"""Re-send every received item's command to the game (use if items seem to have not applied after a level load)."""
		self.output("Resyncing all received items to the game.")
		self.ctx.write_all_commands()


class JediAcademySPContext(CommonContext):
	command_processor = JediAcademySPCommandProcessor
	game = "Jedi Academy SP"
	items_handling = 0b111  # full remote

	def __init__(self, server_address, password):
		super().__init__(server_address, password)
		self.game_path = find_openjk_homepath()
		self.qconsole_path = os.path.join(self.game_path, "qconsole.log")
		self.commands_path = os.path.join(self.game_path, "ap_commands.txt")
		self._log_read_pos = 0
		self._sent_checks: set[str] = set()
		self._mission_completions_seen: set[str] = set()

	async def server_auth(self, password_requested: bool = False):
		if password_requested and not self.password:
			await super().server_auth(password_requested)
		await self.get_username()
		await self.send_connect()

	def on_package(self, cmd: str, args: dict):
		if cmd == "Connected":
			os.makedirs(self.game_path, exist_ok=True)
			self.write_all_commands()
		elif cmd == "ReceivedItems":
			self.write_all_commands()

	def write_all_commands(self):
		"""Rewrites ap_commands.txt from scratch with the command for every
		item received so far. Always a full rewrite, never an incremental
		append - avoids any race with the game's read-then-clear poll cycle
		(worst case with a full rewrite is the game picks it up one poll
		late, not a lost/corrupted write)."""
		lines = []
		progressive_counts: dict[str, int] = {}
		for network_item in self.items_received:
			item_name = self.item_names.lookup_in_game(network_item.item)
			if item_name in ITEM_TO_GAME_COMMAND:
				lines.append(ITEM_TO_GAME_COMMAND[item_name])
			elif item_name in PROGRESSIVE_ITEM_NAME_TO_SVCMD:
				svcmd = PROGRESSIVE_ITEM_NAME_TO_SVCMD[item_name]
				progressive_counts[svcmd] = progressive_counts.get(svcmd, 0) + 1
			# filler items have no ITEM_TO_GAME_COMMAND entry and aren't
			# progressive either - intentionally no-op, nothing to send.
		for svcmd, count in progressive_counts.items():
			lines.append(f"ap_set{svcmd} {count}")

		tmp_path = self.commands_path + ".tmp"
		with open(tmp_path, "w") as f:
			f.write("\n".join(lines) + "\n" if lines else "")
		os.replace(tmp_path, self.commands_path)

	@property
	def endpoints(self):
		return [self.server] if self.server else []

	def run_gui(self):
		from kvui import GameManager

		class JediAcademySPManager(GameManager):
			logging_pairs = [("Client", "Archipelago")]
			base_title = "Archipelago Jedi Academy SP Client"

		self.ui = JediAcademySPManager(self)
		self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx: JediAcademySPContext):
	while not ctx.exit_event.is_set():
		if not os.path.exists(ctx.qconsole_path):
			await asyncio.sleep(1)
			continue

		with open(ctx.qconsole_path, "r", errors="ignore") as f:
			f.seek(ctx._log_read_pos)
			new_lines = f.readlines()
			ctx._log_read_pos = f.tell()

		new_checks = []
		resync_needed = False
		for line in new_lines:
			server_match = SERVER_MAP_RE.search(line)
			if server_match:
				# Fresh level load - force power state (and possibly more)
				# just got reset. Re-send everything so far.
				resync_needed = True
				continue

			check_match = CHECK_REACHED_RE.search(line)
			if not check_match:
				continue
			check_id = check_match.group(1)
			location_name = CHECK_ID_TO_LOCATION_NAME.get(check_id)
			if location_name is None:
				continue  # e.g. a force-power-menu check, not a real AP location
			if check_id in ctx._sent_checks:
				continue
			ctx._sent_checks.add(check_id)
			new_checks.append(location_name_to_id[location_name])

			if check_id.startswith("mission_complete_"):
				ctx._mission_completions_seen.add(check_id)

		if resync_needed:
			ctx.write_all_commands()

		if new_checks:
			await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])

		if not ctx.finished_game and len(ctx._mission_completions_seen) >= MISSION_COMPLETE_COUNT:
			await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
			ctx.finished_game = True

		await asyncio.sleep(1)


if __name__ == "__main__":
	async def main(args):
		ctx = JediAcademySPContext(args.connect, args.password)
		ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
		if gui_enabled:
			ctx.run_gui()
		ctx.run_cli()
		watcher = asyncio.create_task(game_watcher(ctx), name="JediAcademySPGameWatcher")

		await ctx.exit_event.wait()
		ctx.server_address = None

		await watcher
		await ctx.shutdown()

	import colorama

	parser = get_base_parser(description="Jedi Academy SP Client, for text interfacing.")
	args, rest = parser.parse_known_args()
	colorama.init()
	asyncio.run(main(args))
	colorama.deinit()
