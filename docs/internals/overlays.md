# THPS2 front-end overlays

The menu screens of Tony Hawk's Pro Skater 2 are not in the main image. Each is a small relocatable MIPS program stored in the ROM
tail after the asset tree, with a relocation stream, loaded on demand by the game. This page records the format, the loader, and how
the port translates and runs them. Facts only: addresses, sizes, names. Labels: **[V]** verified by `decomp/common/overlay_table.py`,
`overlay_relocs.py` or a run, **[I]** inference.

## The 16 screens [V]

The table in main `.data` at `0x800EB2F0` (USA; Europe `0x800EB3B0`) has 16 records of 28 bytes. The names:
`t2_menuwheel` (the wheel main menu), `t2_loadcareer`, `t2_equipsel`, `t2_buystatsmenu`, `t2_tricked`, `t2_ingamesave`, `t2_options`,
`t2_frontload`, `t2_levelselect`, `t2_displevelgoals`, `t2_playerselmenu`, `t2_createsktr`, `t2_2phandicap`, `t2_2playergamemenu`,
`t2_intro` and `edmod` (the park editor, the largest by far: about 0x15E28 bytes of code plus a 0x2098-byte relocation stream).

A record is: name pointer, code ROM address and size, relocation-stream ROM address and size, and two zero words (cache-operation
ranges, zero in every record). The 16 code and relocation pairs tile the ROM tail `0xF587B6-0xFA4E22` (USA) exactly. ROM addresses
in the table are *link-time* ones: the tail was linked as if it followed the uncompressed code (`0xFB980` bytes), so the loader
shifts them by `0xFB980 - [0x80011C7C]`, where `[0x80011C7C]` is the asset-root word that boot copies (`0x821BA` for USA). [V]

## The loader [V]

| Role | USA address | Notes |
|---|---|---|
| `Overlay_Load(name)` | `0x80096E30` | looks the name up, allocates code and relocation buffers from the heap (0x40 aligned), reads both through the PI DMA queue in 0x800-byte chunks, relocates, then calls offset 0 of the blob with the screen object |
| `Overlay_Reloc(base, stream)` | `0x80097070` | applies the relocation stream |
| `Overlay_Call(name, cmd, a, b)` | `0x800971A4` | finds the loaded screen and calls its slot `cmd`; this is how a screen runs each frame |
| `Overlay_Unload(name)` | `0x800972FC` | calls the screen's destructor slot, frees the blob and unlinks it |
| screen node list head | `0x800EB4B0` | a doubly linked list; slot pointers live in the node |

The blob starts with an init function that stores the screen's methods into the descriptor, then the screen's code; strings and tables
follow the code. Stubs in the main image load the screens by name, four small functions per screen.

**The load address is not fixed.** The same screen was seen at `0x801689C0`, `0x8016C740`, `0x802CE080` and `0x80445480` in one
session, because the heap moves. A flat recompile at one address would fail on the second visit.

## The relocation stream [V]

Big-endian 32-bit words until `0xFFFFFFFF`; `type = word & 3`, `site = word & ~3` (a byte offset into the blob).

| Type | Name | Action | Extra word |
|---|---|---|---|
| 0 | R_MIPS_32 | `*(u32*)site += base` (data pointers: vtables, string and function tables) | none |
| 1 | R_MIPS_HI16 | immediate = `(base + A + 0x8000) >> 16` | A, a blob offset |
| 2 | R_MIPS_LO16 | immediate = `(base + A) & 0xFFFF` | A |
| 3 | R_MIPS_26 | `*(u32*)site += (base & 0x0FFFFFFF) >> 2` (internal `jal` and `j`) | none |

Every relocation targets the blob itself. Absolute `jal`s into the main image are *not* relocated: all 328 distinct targets in the
main `.text` are function starts in `recomp/thps2.syms.toml`, which is strong evidence that the tail is real MIPS code linked against
exactly this main image. About 84 of those targets have no static caller in the main image and are reached from the overlays only. [V]

## How the port runs them

N64Recomp has a relocatable-section model (it is how Zelda64Recomp handles its overlays), and the four relocation types above map
one to one onto its section `relocs` (HI16, LO16, 26, 32). So:

1. `decomp/common/overlay_recomp.py` decodes each stream, finds the functions (offset 0, `jal` targets, address values after a
   `jr ra`, then a linear sweep; jump tables through the LO16 relocation that points at a run of R_32 words), pre-links the blob at a
   fake base, appends it to the class's code blob, and writes an N64Recomp section with its `relocs`. Result: **552 functions in 16
   sections, 0 warnings** with the main program (3,908 functions per release).
2. At run time the game's own loader still relocates the words in RDRAM (data pointers, vtables), and the recompiled code reads
   them from RDRAM. The host's PI-DMA hook compares every ROM read at or above `0xF58000` with the overlay table; the read that starts a
   blob calls `load_overlays(blob_offset, destination, size)`, which registers the functions at the address the loader chose, after
   unloading any registered overlay that overlaps or is the same screen. Overlay functions are named `ovl_<screen>_<offset>`.
3. Section registration passes the total section count as well as the pointer (librecomp sizes a table from it).

Findings worth keeping: the relocation list must be **sorted by address**, not by type, because N64Recomp walks it with a moving index
(with the wrong order only 17 of the LO16 relocations were applied); and a string pointer after a `jr ra` looks like a function start,
so pointer-derived starts are limited to the code range.

## At first run (the split build)

The downloaded app has no Python, so the half of `overlay_recomp.py` that reads the ROM is C++: `decomp/common/firstrun/overlay_rom.cpp`.
It takes the **recipe** (`recomp-host/recipes/<class>/overlays.txt`: screen names, ROM offsets and sizes of each blob and relocation stream,
the function map, and an XXH3-64 fingerprint of the ROM range they cover; no ROM bytes) and your ROM, checks the fingerprint (a modified dump is
refused with a message), then makes the same three things the Python tool makes: the code blob with the pre-linked overlays appended, the
`[[section]]` symbol text and the overlay table. The output is byte-identical to the static build's input; `decomp/common/firstrun/test_overlay_rom.py`
checks that, and that the recipes contain no ROM bytes. The N64Recomp and RSPRecomp configs are generated at package time from the committed
version tables, so they are not part of the recipe.

---
Unofficial. This project is not affiliated with Activision, Neversoft, Edge of Reality, Tony Hawk or Nintendo. Facts derived
from analysis of retail cartridge dumps. No game data is reproduced beyond names, addresses and individual values. See the README.
