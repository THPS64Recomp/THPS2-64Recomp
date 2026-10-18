# THPS2 recomp host (N64: USA and Europe)

The native macOS (arm64) host for Tony Hawk's Pro Skater 2 for N64, made with
[N64Recomp](https://github.com/N64Recomp/N64Recomp) and run on N64ModernRuntime + RT64 (Metal). This is the developer
README. Users want the top-level [README](../../../README.md) and [docs/MANUAL.md](../../../docs/MANUAL.md).

> **No ROM data is in this directory.** The recompiled C, the code blob, dumps, reference frames and build output are all
> generated locally from your own dump and are git-ignored (`build/`, `*.png`, `*.bin`). `versions/` and `recipes/` hold addresses, offsets,
> names and hashes only (the per-class overlay tables included). This directory holds our configs, small tools and notes; the C++ is in `../../common/host/`.

How it works inside: [docs/internals/recomp.md](../../../docs/internals/recomp.md). The two releases:
[docs/internals/versions.md](../../../docs/internals/versions.md). The front-end screens:
[docs/internals/overlays.md](../../../docs/internals/overlays.md). What has been verified:
[docs/VERIFICATION.md](../../../docs/VERIFICATION.md).

## Layout

The host (sources, CMake file, Python tools, test harness, RT64 patches) is shared by THPS1-3 and lives in `../../common/host/` (ADR 0006); this
directory is the game's profile. `tools/` and `tests/` here hold small wrappers with the shared tools' names, so the commands below run from this
directory. Where this README says `src/x.cpp`, it is `../../common/host/src/x.cpp`.

```
CMakeLists.txt            9 lines: project(), THPS_FAMILY, THPS_SKIP_INTRO overlay, include(../../common/host/cmake/thps_host.cmake)
game/game.toml            the game profile: names, config folder, wording, flags (-> thps::game in build/gen/thps_versions.h)
game/game_hooks.def       the hook functions only this game's N64Recomp config calls
config/thps2.hooks.toml   N64Recomp [[patches.hook]] blocks (loader, PI, events, widescreen, skip intro, region check), by function name, all classes
config/thps2.aspMain.toml RSPRecomp config template for the audio microcode
versions/                 classes.toml, host_syms.toml (the names the host needs), <class>/{host_force,data_syms}.toml and overlay_table.inc
recipes/<class>/          committed ROM-free first-run inputs: `thps2.host.syms.toml`, `blob.txt`, `overlays.txt` (the 16 front-end screens' layout and function map)
tools/gen.py              wrapper -> ../../common/host/tools/gen.py: per class syms -> overlays -> N64Recomp -> namespace; RSPRecomp (build/gen/, local)
tools/gen_versions.py     validates the version tables; writes build/gen/thps_versions.h, per-class N64Recomp configs
tools/build_host.py, test.sh, package_split.py, scan_bundle.py, setup_runtime.py ...   wrappers of the shared tools
tests/scenarios.py        this game's checkpoints and input scripts (the shared runner and harness are in ../../common/host/tests/)
../../common/host/src/    main, hooks, input, audio, pak, widescreen, interpolation, rom_check, versions, the first-run flow, the split build, the menu ...
../../common/host/patches/   our RT64 patches (applied by tools/setup_runtime.py)
../../common/overlay_recomp.py   front-end overlays as relocatable sections (static build); ../../common/firstrun/ the same from the user's ROM (first run)
```

## Build

The one-command route (macOS, Windows, Linux), once per game dump you want to build:

```sh
python3 -I tools/build_host.py --rom /path/to/Tony-Hawk-Pro-Skater-2-USA.z64 --rom /path/to/Tony-Hawk-Pro-Skater-2-Europe.z64
```

It fetches the pinned N64ModernRuntime and RT64 and applies our patches (`tools/setup_runtime.py`), builds N64Recomp and RSPRecomp
at the pinned commit, makes a Python venv with `rabbitizer`, inflates each ROM's code and generates the C for each code class
(`tools/gen.py`), then configures and builds the host with CMake and Ninja. `--stub` builds with ROM-free stand-in functions to
check the toolchain. A build with only the USA ROM runs USA only.

By hand, once the runtime tree is in `<runtime-dir>`:

```sh
cd decomp/thps2
make extract ROM_SRC=/path/to/thps2-usa.z64 && make recomp-inputs      # USA: baserom.*, build/thps2.codeblob.bin
.venv/bin/python -I recomp-host/tools/seed_class.py eu /path/to/thps2-europe.z64 --src-rom baserom.z64 --src-main baserom.main.bin
cd recomp-host
python3 -I tools/gen.py /path/to/N64Recomp    # per class: 3,908 functions (3,356 + 552 in the 16 overlays), 0 warnings
cmake -S . -B build/cmake -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DRECOMP_RUNTIME_DIR=<runtime-dir>
cmake --build build/cmake                       # CMake links every class under build/gen/*/
```

Prerequisites on macOS: Xcode (or the Command Line Tools) with the Metal toolchain, Homebrew `cmake ninja sdl2 pkgconf`.

## Split build: no game code in the app

`-DTHPS_SPLIT_GAME_LIB=ON` builds the engine without any recompiled game code. On first run the app translates the user's ROM with the bundled
N64Recomp and RSPRecomp, compiles the C with the system compiler and loads `<config>/game/thps2_game_<class>.<dylib|so|dll>`. This is how releases
are built. `recipes/us` serves the USA dump and `recipes/eu` the Europe dump; the app picks the recipe by hash. The front-end screens are read from the user's ROM with the recipe's layout
([docs/internals/overlays.md](../../../docs/internals/overlays.md#at-first-run-the-split-build)). The design, shared with THPS1, is in the THPS1
repository's `docs/internals/recomp.md`. Files: `src/game_split.cpp`, `src/firstrun.cpp`, `../../common/firstrun/overlay_rom.cpp`, `game-lib/`,
`tools/package_split.py` (assembles the `.app`; one zip per game with all its recipes), `tools/scan_bundle.py` (the ROM-byte scan).
`tests/firstrun_test.py` builds from a dump on a clean config folder and then plays.

## In-game settings menu

Esc (controller: Back) opens an RmlUi menu over the game (General, Controls, Graphics, Sound) that edits `general.cfg`, `graphics.cfg` and
`controls.cfg`. The code is shared by all three games;
its libraries and fonts are fetched by `tools/setup_runtime.py` at pinned hashes, never stored. `-DTHPS_MENU=OFF` builds without it.

## Supported ROMs

One binary runs both releases; it identifies the file by hash (so `.z64`, `.n64`, `.v64` all work) and keeps a copy per
version in the config folder (`<game id>.z64`). `build/cmake/thps2_recomp --check-rom FILE` says what a file is. Hashes are of the
big-endian ROM.

| Release | Header (name, code, rev) | SHA-1 | MD5 | XXH3-64 | Code class | Status |
|---|---|---|---|---|---|---|
| USA | `THPS2`, NTQE, 0 | `458ac754cd8e08c46f4c5c9204192ecde84a179d` | `29974692808c112b306fbd259273dc96` | `8E5ABB6C1CE403DB` | `us` | supported |
| Europe | `THPS2`, NTQP, 0 | `803672c1ffa7860536d8b35dca8b59f637f4165e` | `6be030475c4db52f273ef8a02b4dafa8` | `F32FEE0FC9FE5F6A` | `eu` | supported at NTSC timing |

- Europe is a **re-link** of the USA program (its own recompiled payload and overlays; 6 of 3,101 main functions and 8 of the 16
  front-end screens differ beyond relocation). English only, like USA; no language select.
- It runs with `osTvType = NTSC`: the runtime paces retraces at 60 Hz and the frame sizes are NTSC's. `--tv pal|ntsc|mpal`
  overrides; PAL is experimental (a PAL-sized picture with 60 Hz pacing).
- **Region check.** Both releases compare the console's TV type with their own region (`Tv_IsHomeRegion`) and show "THIS GAME IS
  NOT DESIGNED FOR USE ON THIS SYSTEM" on a mismatch, which is what Europe does at NTSC timing. The host is a region-free console: a
  hook makes that test always pass, for every version (`config/thps2.hooks.toml`).
- What differs on Europe: the Activision O2 "Sports Revolution" logo on the title screen, the shorter Nintendo legal text,
  "press start to access the menu", the controller-missing message, and the main menu's "CAREER MODE" label sits one pixel lower-left.

## Run

```sh
build/cmake/thps2_recomp --rom /path/to/thps2-usa.z64
build/cmake/thps2_recomp --version thps2_eu        # a stored ROM of another version (default: the first one stored)
```

The ROM is identified by hash and a copy is kept in the config dir as `<game id>.z64` (`~/Library/Application Support/THPS2-64Recomp`,
or the folder holding a `portable.txt`; `--config DIR` overrides), so later runs need no `--rom`. Controller Pak saves go to
`<config>/saves/thps2_pak1.mpk` (a standard 32 KiB `.mpk`). The binary is `thps2_recomp`.

Flags: `--mute`, `--wav`, `--no-pads`, `--windowed/--fullscreen`, `--aspect`, `--window`, `--res-scale`, `--msaa`, `--refresh`,
`--skip-intro`, `--show-fps`, `--volume`, `--controls-preset`, `--verbose`, `--control`, the dump flags, and `--unlock-levels` (a
test aid: levels 0 to 9 selectable in a fresh career, not saved); see the header of `src/main.cpp`. Graphics defaults: 16:9, a
1280x720 window, auto resolution scale, 4x MSAA, interpolation to the display rate. The settings tables are in
[docs/MANUAL.md](../../../docs/MANUAL.md).

### Controls

THPS2's pad layer (a PlayStation-style one) takes N64 buttons like this:

| N64 button | pad record | THPS2 action |
|---|---|---|
| C-down | 3 | ollie |
| C-left | 1 | flip |
| C-right | 2 | grab |
| C-up | 0 | grind |
| **A** | 3 | ollie too (and menu accept) |
| **B** | 1 | flip too (and menu back) |
| L / R | 4+5 / 6+7 | spin left + nollie / spin right + switch |
| START | 14 | pause |

There is no revert button. Manuals are stick up/down with no button (up, down = manual; down, up = nose manual). The default
`thps-xbox` preset puts south = ollie (sends N64 A + C-down), west = flip, east = grab (C-right, plus N64 B outside the level),
north = grind. Because the game reads N64 B as **flip** in the skating code, the host drops that B while the skater is under control
(the game's own "level run being played" flag) and drops C-right instead on every other screen; in every menu east = back, also in the
pause menu (it resumes) and in Create-a-Skater. `--controls-preset n64`
is the plain N64 layout. Bindings are in `<config>/controls.cfg`.

### Skip Intro, Show FPS, crash log

`--skip-intro` (or `skip_intro = 1` in `general.cfg`) presses B on the "EXPANSION PAK FOUND." box and skips the legal text (a hook on
the intro overlay's update), so the game boots to the logo screen in about 2 s instead of about 25 s. START on the title opens
the main menu wheel. `--show-fps` puts the counter in the window title. A crash writes `<config>/crash.log` with the recompiled
game function names.

## How the boot works (differences from THPS1)

1. The same IPL3 emulation and entrypoint wrapper: `load_overlays(0x13B70, 0x80016B20, 0xE7E10)` re-registers the main image;
   `Boot_Main` runs recompiled with `Boot_PioCopy` and `Erz_UnpackMethod1/2` hooked (all 15 chunks are method 2). The PIO copy
   rounds a chunk down to whole words, so THPS2's last chunk loses 2 bytes; the hook completes the copy from the ROM.
2. The game's DMA thread (`Pi_DmaThread` at `0x800CF294` in USA) uses `osPiRawStartDma`, hooked as in THPS1.
3. **Front-end overlays.** The 16 menu screens are blobs in the ROM tail, loaded to heap addresses that vary from run to run and
   relocated by the game's own loader. They are recompiled as N64Recomp relocatable sections; the PI-DMA hook calls `load_overlays`
   when a screen's blob is read ([docs/internals/overlays.md](../../../docs/internals/overlays.md)).
4. Audio, Controller Pak, the scissor edge fix, widescreen and interpolation work as in THPS1, with THPS2 addresses (`config/*.toml`).

## Tests

```sh
tools/test.sh --record          # first time on a machine: capture reference frames (ROM-derived, build/tests/refs)
tools/test.sh                   # controls.cfg test + the whole suite
tools/test.sh --only pak_save   # one scenario (+ the ones before it in its session)
tools/test.sh --check-refs      # how distinct the recorded references are
tests/run.py --version thps2_eu # the suite on Europe (its references live in build/tests/refs-thps2_eu/; the rest fall through to USA's)
```

`tests/run.py` starts the host once per **session** and walks the game through **scenarios**, waiting for **checkpoints**
instead of sleeping. Only one `thps2_recomp` runs at a time (`--no-pads --mute`; `uptime` is logged with every number). The scenarios cover the
front end, a career level, audio, controls, widescreen, Controller Pak, the settings, the camera and aspect checks, high frame rate and the
in-game settings menu (`menu` and `menu-reload` sessions, six scenarios, skipped when `--features` says `menu=0`).

Full runs on the static build, 2026-10-12: Europe 32 pass, 0 fail, 4 skipped; USA 32 pass, 0 fail, 4 skipped, after re-running `level_grab`, a
known flake (the in-level HUD checkpoint was missed under load; `pause_resume` failed about one run in three in earlier runs). The 4 skips are
launcher-only scenarios. The split-built Europe library passed the full suite (26/0/4) before the menu scenarios were added, and
`tests/firstrun_test.py` passes for both releases. Game addresses (pad layer, skater pointer) are read by name from the running version, never
hard-coded in the scenarios.

## Windows and Linux (ported, not yet run on either)

The same host code and platform seams as THPS1 (`src/platform.{h,cpp}`, `crash.cpp`, `create_window()`), the same flags (`--api`,
Alt+Enter) and the same tools: `tools/build_host.py`, `tools/build_windows.ps1`, `tools/setup_runtime.py`, and `-DTHPS_STUB_FUNCS=ON`
with `tools/gen_stub.py` for a ROM-free build. `tools/mingw_check.py` cross-compiles the whole host, menu included, with MinGW, and the manual
CI (`.github/workflows/ci.yml`) builds the stub host on Linux, Windows and macOS; both pass. No real Windows run has been done yet. Test kit:
[docs/WINDOWS-TEST.md](docs/WINDOWS-TEST.md). Config folder: `%LOCALAPPDATA%\THPS2-64Recomp`.

## Not done

- No in-game pak swapping; the in-game pak manager is not exercised by the tests; Rumble Pak output is untested on a real pad.
- Widescreen: the in-level HUD is anchored to the screen edges by default (`--hud expand`; `--hud original` keeps it centred 4:3); menus and loading screens are pillarboxed.
- High frame rate is checked in The Hangar only.
- Texture packs: not attempted. The settings menu has no rebinding of single keys or buttons yet (edit `controls.cfg`).
