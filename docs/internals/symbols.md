# THPS2 symbols: coverage, sources and evidence

How the function and data names in `decomp/thps2/symbols/{boot,main}.txt` came about, how much is named, and how far to trust each
name. Names are identifiers only; no code from any reference project is used.

## Coverage

| Segment | Named | How |
|---|---|---|
| Boot segment (libultra, IDO) | 233 of 253 | n64sym's built-in signatures (exact byte match); the loader functions by hand |
| Main image | 214 of 3,101 (80 with a `_maybe` suffix) | n64sym hits for libgcc, libmus and n_audio; names carried over from THPS1 by body matching; hand identification |
| Function bounds | all 3,354 set | `recomp/thps2.syms.toml`, checked by `make recomp-check` |

Boundaries matter more than names for N64Recomp: it needs every function start and size to be right, not every name. By category
the named main functions are skater and tricks 53, camera 12, loading and assets 29, audio
libraries 31 and other 89.

## Where the names come from

<!-- table-ok: the name sources in priority order -->
| Tag in `symbols/*.txt` | Source | Trust |
|---|---|---|
| `loader` | hand-read Edge of Reality loader (`Boot_Main`, `Boot_PioCopy`, `Erz_*`) | high |
| `n64sym` | shygoo's n64sym built-in signatures: libultra (IDO) in boot, libmus, n_audio and libgcc in main | high (exact bytes); tiny hits inside game code are vetted against THPS1's accepted set |
| `manual` | read in the disassembly: `Pi_DmaThread`, `osAiGetStatus`, `View_SetFrustum`, `View_ComputeCullPlanes`, `DoPhysics`, `Trick_Land`, `Trick_Bail`, `Vibrate`, `GGame` | medium-high |
| `sigmatch-A` | a THPS1 function with an identical masked body, unique on both sides | high |
| `sigmatch-O` | identical bodies resolved by link order between A anchors | medium |
| `sigmatch-C` | callee of a matched function, at least 50 % body agreement; the name gets `_maybe` | low-medium |
| `sigmatch-F` | fuzzy shingle containment (a modified function); `_maybe` | low |

`decomp/common/sigmatch.py` masks the jump targets and 16-bit immediates of the ALU-immediate ops and loads/stores, then looks for
the whole masked body. Validation: tier A agrees with the independent function-list pass on 872 of 886 starts (the 14 others are
libmus F-commands and `__osException`).

The PS1 *Tony Hawk's Pro Skater 2* demo decompilation (emoluvjd; no licence granted for its code) was used as a **naming reference
only**, for a handful of names (the PS1 demo is an earlier build than the N64 final). No code, header or data was copied, and nothing
from that repository is part of this one. THPS1's names are the vocabulary for most of THPS2's. No leaked source code was used.

## Jump tables and vtables

- 78 non-`$ra` `jr` in `.text`; N64Recomp turned 74 into `switch` statements (all jump tables). 2,036 jump-table case pointers live in
  `.rodata`.
- 122 GCC 2.x vtables (8-aligned `{0,0}` header, then `{delta, pfn}` per slot); every slot is a listed function. Four-slot
  front-end screen tables sit at `0x800174C0`, `0x80017558`, `0x80017590`, `0x800175D8`, `0x80017630` and `0x800176B0`, and
  twelve-slot object tables at `0x80017030`, `0x80017430` and `0x80019148`. Class names do not transfer from THPS1 (1 of 11 named
  vtables mapped): the class methods changed.

## Still unnamed

THPS2 rewrote the trick-handling code (the `HandleTricksNew` family, `Trick_TakeOff`, `Trick_Trick`, the rail-grind start, the manual code
and the specials), so no signature survives. Anchors for anyone continuing: the physics translation unit around `0x8007D3E0` to
`0x80090C98` (116 functions), `Trick_Land` `0x8007DB9C`, `Trick_Bail` `0x8007DEF0`, `DoPhysics` `0x8008E698` and `GGame` `0x800F84D0`.

---
Unofficial. This project is not affiliated with Activision, Neversoft, Edge of Reality, Tony Hawk or Nintendo. Facts derived
from analysis of a retail cartridge dump. No game data is reproduced beyond names, addresses and individual values. See the README.
