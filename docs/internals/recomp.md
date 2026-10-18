# How the THPS2 recomp works

The internals of the native port of Tony Hawk's Pro Skater 2 (N64): what the translator needs, how the host boots the game, and
what differs from the THPS1 port. Addresses are USA unless a release is named; see [versions.md](versions.md) for Europe and
[overlays.md](overlays.md) for the front-end screens. Labels: **[V]** verified by a script, test or by reading the code;
**[I]** inference. Since ADR 0006 the host sources are shared by THPS1-3: `src/x.cpp` in this page is `decomp/common/host/src/x.cpp`, and the game's own
files are its profile in `decomp/thps2/recomp-host/` (`game/game.toml`, `versions/`, `config/`).

## 1. Pipeline

```
your dump (.z64/.n64/.v64) --hash check--> inflate the 15 code chunks (native ERZ decoder, method 2)
   --> code blob: ROM[0:0x1000] | boot segment | inflated main image | the 16 pre-linked overlays   (stays on your machine)
   --> N64Recomp + the function list (recomp/thps2.syms.toml, our hooks)    --> 3,908 functions of C per release
   --> RSPRecomp + config/thps2.aspMain.toml                                --> the audio microcode as C++
   --> system compiler                                                      --> the game code
engine (host + N64ModernRuntime + RT64 + SDL) runs it.
```

- **N64Recomp** (`ffb39cd`, the same pin as THPS1) reports **0 warnings** on the function list: 3,354 functions of the main program
  (253 boot, 3,101 main) plus 552 in the overlays, and two starts the host adds. [V]
- The recompiler's config (`recomp/thps2.recomp.toml`) has entry point `0x80000400`, nine instruction patches (PlayStation
  coprocessor-2 leftovers turned into no-ops, all in one function at `0x80045270`), and the `[[patches.hook]]` blocks of
  `config/thps2.hooks.toml`, by function name and shared by both releases.
- N64Recomp's symbol-file mode needs the entry function at ROM `0x1000`, so the main part of the blob is `ROM[0:0x1000]`, the boot
  segment at blob `0x1000` and the inflated main image at blob `0x13B70` (vram `0x80016B20`). [V]
- Stubs the host must provide (`recomp/runtime_stubs.txt`): 16 libultra internals that the generated code calls and the runtime
  does not (`__osContRamRead`, `__osPfsRWInode`, `osPiRawStartDma`, ...).
- The generated C is ROM-derived. It is never committed and never shipped.

## 2. The function list

`decomp/common/funclist.py` and `gen_syms.py` make the list: 3,354 functions in the main program. Strong starts are `jal` targets
from both images, data pointers to a prologue, to the instruction after a return, or to a 16-aligned address after padding, section
starts and curated symbols; weak starts are dropped when an earlier function branches across them. Linker padding is recognised
by its garbage opcodes. Static checks (`recomp_check.py`): nothing lies outside a function except padding; 74 of the 78 indirect
jumps become `switch` statements (the other 4 are libultra's, which the runtime reimplements); 335 indirect-call sites go through
the runtime's function lookup; 521 `do_break` calls come from division checks. [V]

## 3. Boot

1. librecomp's IPL3 step copies ROM `0x1000` plus 1 MiB to `0x80000400`. That is right for the boot segment and wrong for the
   main image, so our `GameEntry.entrypoint` wrapper unloads those sections and re-registers the main image at `0x80016B20`
   (`load_overlays(0x13B70, 0x80016B20, 0xE7E10)` for USA).
2. `Boot_Main` runs as recompiled code: BSS clear, `osInitialize`, the chunk-table read and the 15-chunk inflate loop, then `GameEntry`
   (`0x800B6AF8`). Its hardware-touching leaves are hooked: `Boot_PioCopy` becomes a ROM-to-RDRAM copy, and the ERZ decoders become the
   native decoder in `src/erz.cpp`. The original copy rounds a chunk down to whole words and so loses 2 bytes of the last chunk;
   the hook completes the copy from the ROM. [V]
3. The game's DMA thread (`Pi_DmaThread`, `0x800CF294`) reads assets with `osPiRawStartDma` and waits on a cartridge event. The
   runtime's version is a fatal stub and its `osSetEventMesg` ignores those events, so both are hooked: the DMA copies from the ROM
   and posts the registered message. The same hook watches for reads from the overlay area ([overlays.md](overlays.md)).

## 4. The rest of the host

The host is THPS1's, ported: the long explanations of frame pacing, audio pacing, the scissor edge fix and the high-frame-rate code
apply unchanged, with THPS2 addresses.

- **Frame pacing and audio.** The game's scheduler is a standard libultra-style one driven at a steady 30 fps; `n_aspMain` is
  translated by RSPRecomp and the audio thread produces a buffer whenever `osAiGetStatus` says the FIFO is not full.
- **Input** (`src/input.cpp`) and **Controller Pak** (`src/pak.cpp`, the `osPfs*` file API on a real `.mpk` layout; a career save
  is a note of 6,816 bytes). THPS2 reads N64 B as flip in the skating code, so the default Xbox-style layout drops the B that the
  east button sends while the skater is under control (the game's run flag `gRunActive`, `src/run_state.cpp`); on every other screen it drops
  C-right instead, so east is back in every menu, also the ones that draw a 3D scene.
- **Widescreen** (`src/widescreen.cpp`): the frustum and culling are widened (`View_SetFrustum` `0x800C0D3C`,
  `View_ComputeCullPlanes` `0x800C1838`; the view struct is THPS1's) and RT64 widens the projection; the in-level HUD goes to the screen edges by default (`src/hud_anchor.cpp`; `--hud original` keeps it centred 4:3).
  **Frame interpolation** (`src/interpolation.cpp`): RT64 renders in-between frames, the host tells it the game's rate (30) and
  tags camera cuts.
- **Skip Intro** (`src/skip_intro_overlay.cpp`): a hook on the intro screen's update, which lives in an overlay, so Skip Intro's hook target
  is named per release ([versions.md](versions.md#names-inside-overlays)).
- **PAL and the region check.** Both releases compare the console's TV type with their own region (`Tv_IsHomeRegion`: `0x800B6818`
  in USA, `0x800B6848` in Europe) and stop at "this game is not designed for use on this system" on a mismatch. The host is a
  region-free console, so one hook (`ctx->r2 = 1; return;`, for every release) makes the test pass. The host runs every release at
  NTSC timing (the runtime paces retraces at 60 Hz; `osTvType` still chooses the video mode and `--tv` overrides it). [V]

## 5. Differences from THPS1 in short

- 15 ERZ chunks of method 2 (THPS1: 14 of method 1); a 16 MiB ROM; a different loader layout (`Boot_PioCopy` `0x80000AB4`,
  `Erz_UnpackMethod2` `0x80000C50`, `Erz_UnpackMethod1` `0x80001340`).
- 16 relocatable front-end screens in the ROM tail, which THPS1 does not have.
- Two releases with different code, so two code classes (`us`, `eu`) in one binary.
- No revert button. The first-run (split) build reads the front-end screens from the user's ROM with a ROM-free recipe ([overlays.md](overlays.md#at-first-run-the-split-build)).

## 6. Platforms

macOS (Metal) is the only system the game has been played on. The Windows and Linux support is written and built in CI with
ROM-free stand-in functions: OS seams in `src/platform.{h,cpp}`, `src/crash.cpp`, `create_window()` in `src/main.cpp` and the CMake
file, structured after Zelda64Recomp's `main.cpp` (credits in [NOTICE](../../NOTICE.md)). Config folders: macOS
`~/Library/Application Support/THPS2-64Recomp`, Windows `%LOCALAPPDATA%\THPS2-64Recomp`, Linux `$XDG_CONFIG_HOME` or
`~/.config/THPS2-64Recomp`; a `portable.txt` beside the executable overrides them.

## 7. Building the host from source

`python3 -I decomp/thps2/recomp-host/tools/build_host.py --rom USA.z64 --rom EUROPE.z64` does everything: the pinned runtime and RT64
plus our patches, N64Recomp and RSPRecomp at the pin, a venv with rabbitizer, the code blobs, `tools/gen.py`, then CMake and Ninja.
By hand and per-option details: [the host README](../../decomp/thps2/recomp-host/README.md).

---
Unofficial. This project is not affiliated with Activision, Neversoft, Edge of Reality, Tony Hawk or Nintendo. Facts derived
from analysis of retail cartridge dumps. No game data is reproduced beyond names, addresses and individual values. See the README.
