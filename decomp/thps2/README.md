# THPS2 (N64) decompilation and recomp groundwork

Tony Hawk's Pro Skater 2 (N64, USA and Europe), ported by Edge of Reality from Neversoft's PlayStation code. This directory turns
your own ROM dump into a byte-identical rebuild from disassembly. It also produces the function list and code blob that N64Recomp
needs. The native host that runs the result is in [recomp-host/](recomp-host/README.md).

> **No ROM data is included or committed.** `baserom*`, `asm/`, `assets/`, `build/`, `linker_scripts/` and `include/` are
> generated locally from your dump and are git-ignored. The repository holds only configs, tools, symbol lists (addresses and
> names) and docs.

| Field | USA | Europe |
|---|---|---|
| ROM | 16 MiB big-endian z64, SHA-1 `458ac754cd8e08c46f4c5c9204192ecde84a179d`, header `THPS2` / `NTQE` / rev 0 | SHA-1 `803672c1ffa7860536d8b35dca8b59f637f4165e`, header `THPS2` / `NTQP` / rev 0 |
| Main image | `0x80016B20`, 15 ERZ method-2 chunks, inflated size `0xE7E10`, SHA-1 `d22dfb9ba81b8777a3294bf14d5538f01200ea97` | inflated size `0xE7ED0`, SHA-1 `06f137c5f19dbbcc9c3ed214ade941f5f3b97992` |
| Front-end overlays | 16 relocatable screens in the ROM tail `0xF587B6-0xFA4E22` ([overlays](../../docs/internals/overlays.md)) | tail from `0xF587F8` |

The decomp rebuild below is for the USA ROM. Europe is covered by the recomp side only ([versions](../../docs/internals/versions.md)).

## Build

Requirements:
- macOS or Linux
- `uv`
- GNU binutils for MIPS (`mips-linux-gnu-*` from Homebrew, or set `CROSS=mips64-elf-`)
- a C compiler
- git

```sh
make setup                                   # venv (splat64 0.50.0) + .deps/rnc_propack_source @499e812
make extract ROM_SRC=/path/to/thps2-usa.z64  # sha1 458ac754cd8e08c46f4c5c9204192ecde84a179d
make                                         # build + verify (prints 3x OK)
make recomp N64RECOMP=/path/to/N64Recomp     # optional: recompile to C in build/recomp/ (0 warnings)
make rsp RSPRECOMP=/path/to/RSPRecomp        # the audio microcode as C++
make recomp-check                            # static completeness checks
```

`make extract` checks the ROM's SHA-1, inflates the main image into `baserom.main.bin` (15 ERZ chunks), runs splat on both
configs, and fixes up the asm (`decomp/common/fix_asm.py`). Regenerate the splat configs with
`python3 -I ../common/gen_splat_cfg.py --game thps2 ROM config`.

## Status

| Target | Result |
|---|---|
| Main image (asm to GNU as/ld) | **byte-identical** (SHA-1 in `checksums/input.main.sha1`) |
| ROM: header + IPL3 + boot asm + original chunks/assets as bins | **byte-identical** (`checksums/build.rom.sha1`) |
| ROM with the main image **built from asm and recompressed** (patched RNC ProPack) | **byte-identical** (`checksums/build.rom_recompressed.sha1`) |
| ERZ recompression of every compressed chunk in the ROM | 1,157 identical (`decomp/common/repack_check.py`) |
| Function list (boot + main) | 3,354 functions (253 boot, 3,101 main), `recomp/thps2.syms.toml` |
| Named functions | boot 233/253; main 214/3,101 (80 `_maybe`) |
| N64Recomp (`ffb39cd`) | runs to completion, **0 warnings**; 9 coprocessor-2 words patched to no-ops |
| Matching C | none |

## Layout

```
config/thps2.{boot,main}.yaml   generated splat configs (offsets only)
symbols/{boot,main}.txt         names (splat symbol_addrs format)
recomp/                         N64Recomp and RSPRecomp configs, generated syms.toml (addresses only), runtime_stubs.txt
                                (thps2_eu.syms.toml: the Europe class)
recomp-host/                    the native host (README inside)
../common/                      shared per-game tools and games.toml
```

Documentation: [recomp](../../docs/internals/recomp.md), [versions](../../docs/internals/versions.md),
[overlays](../../docs/internals/overlays.md), [symbols](../../docs/internals/symbols.md), the data policy in
[game-facts](../../docs/game-facts/README.md). Shared tools: [../common/](https://github.com/THPS64Recomp/THPS64Host/blob/main/TOOLS.md).

## Gotchas shared with THPS1

The compression is RNC ProPack under another magic (method 2 here, method 1 in THPS1); the stock packer reproduces it after the
look-ahead patch in `decomp/common/rnc_propack/lookahead.patch`. The linker filled alignment padding with garbage opcodes
(`fix_asm.py` turns them into `.word`). The RSP microcode is linked inside the CPU `.text`, so splat splits it out and N64Recomp
never sees it. PlayStation coprocessor-2 leftovers sit in one called function. Game logic steps at a fixed 1/30 s.

---
Unofficial. This project is not affiliated with Activision, Neversoft, Edge of Reality, Tony Hawk or Nintendo. See the top-level README.
