from Options import PerGameCommonOptions

# No game-specific options yet - keeping scope tight for a first working
# pass, same staged-scope approach used throughout the ja-sp-src patch this
# session (e.g. secrets were deliberately deferred rather than guessed at).
# Natural candidates for later: an option to also randomize secrets once
# they're extracted from the .bsp files, an option to pick which prologue
# force-power starting state applies, difficulty passthrough (g_spskill).
JediAcademySPOptions = PerGameCommonOptions
