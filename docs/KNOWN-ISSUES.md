# Known issues

What isn't finished or hasn't been checked in v0.1.0-preview. "Untested" means the code exists but hasn't been run in that
setting. Problems fixed before this release are in the [CHANGELOG](../CHANGELOG.md). Found something that isn't here?
[TESTING](TESTING.md) says how to report it.

## Early preview

THPS2 64: Recompiled is an **early preview**. It shares its host with THPS1 64: Recompiled v0.1 and passes its own automated
suite, but it has had much less hand play than THPS1, so this list is likely incomplete. These parts of the game haven't
been played through by a person on this build: the park editor, split screen in a level, replays and most competitions.
[TESTING](TESTING.md) lists what we'd like you to try.

## Platforms

- **macOS (one universal app) and Windows x64 only.** Linux isn't in this release: its code builds in CI, with stand-in
  game code, but has never been run.
- **Intel Macs are untested.** The app's Intel half has only run under Rosetta on an Apple Silicon Mac. Which Intel GPUs
  RT64's Metal renderer supports hasn't been checked.
- **Windows has been tested on one PC:** Windows 11, an Intel Core i7-8809G with AMD Radeon RX Vega M, Direct3D 12, 150 %
  display scaling. Untested: other GPUs (NVIDIA, Intel), Windows 10, other display scaling, and a controller on Windows.
- **Windows: the first start of a new copy is slow to show a picture**, about 4.5 s on the test PC. Later starts are fast.
  It happens with each newly written program file, even with an existing config folder (probably the GPU driver's
  shader cache).
- **Windows: frame pacing is a little less even than on macOS.** Both hold 60 frames per second, but the slowest 1 % of
  frames take about 18.4 ms on the test PC against 16.9 ms on the Mac.
- **The app isn't notarized (macOS) or code-signed (Windows)**, so the first start needs the one-time Gatekeeper or
  SmartScreen step in the [README](../README.md#install).
- **The missing-compiler page** on macOS hasn't been tried on a Mac without the Command Line Tools.

## Game versions

- **USA and Europe are supported** ([MANUAL](MANUAL.md#your-game-dump)), each with its own recipe, because Europe is a
  separate link of the program. Any other release or game is refused.
- **Europe runs at 60 Hz**; the PAL console ran it at 50 Hz. `--tv pal` is experimental (a PAL-sized picture, still paced at
  60 Hz). Real 50 Hz needs a runtime change this project hasn't applied.
- **The region lockout is bypassed** in both releases, so the wrong-region screen never shows.
- **Hand play:** a few sessions of the USA release on macOS and Windows (career save and load, Create-a-Skater, options).
  Europe's front end, which differs from USA's, has been checked mostly by the suite.

## Graphics

- **Widescreen:** the 3D view is widened and the in-level HUD moves to the screen edges (`hud = expand`; `original` keeps
  it in the centred 4:3 area). The HUD keeps its 4:3 size, and a few elements (the timer, trick lines, the pause menu,
  result pages) stay centred on purpose. Menus, loading screens and other 2D screens are pillarboxed 4:3. In **two-player**
  split screen each player's view fills its half of the wide picture, and each player's HUD sits at its own view's edge.
- **Frame interpolation** at 60 Hz and up pairs 97 % or more of the moving parts between game frames in
  the Hangar (the first career level) and the menus. Other levels have cars and other moving objects
  whose pairing hasn't been checked. Replays and cutscenes are untested.
- **Each level start freezes the picture briefly** while the game loads the level (about 0.16 s, 0.2 s in the first
  preview), and the **attract demo** has short stalls every ten seconds or so.
- RT64 **compiles shaders the first time an effect appears**, which causes short hitches.
- With the window hidden or covered, the app stops presenting frames; the game keeps running.
- Apple GPUs have no 8x MSAA; asking for it turns MSAA off.
- **Draw distance:** 2x, 4x and Full were checked on one 15-second ride per course (all at 30 fps), not in long play, two-player
  split screen or replays. At Full the fog is effectively off. A longer distance chosen during a run reaches the far scenery only
  after a RETRY, the next course or a camera change (the game sets that part of the camera only then); a shorter one
  applies at once. No restart is needed.
  Parts of a course the game hides by area appear only as you get near them, as in the original game, and a few far
  pieces the game never drew from that distance can look odd (the Hangar: a dark patch on the far wall).

## Stability

- **A crash in the graphics layer** (inside RT64, seen in all three games under load) is fixed in this release.
  No long soak yet; every suite run plays four courses back to back
  (`course-cycle`), the path of the crash fixed in this release.
## Input and saves

- **Player 2:** by default the first controller to press a button is player 1 and the next is player 2. The Controls
  tab's Controllers list can swap them or give a controller either player; that choice lasts until you quit
  ([MANUAL](MANUAL.md#controls)). The keyboard is always player 1.
- OPTIONS > CONTROLLER 2 opens only for the second controller's A, as in the original game.
- **Cheats are test aids:** off by default. They aren't stored in the Controller Pak save, but progress you make with a
  cheat on (goals, scores, levels unlocked by playing) is saved as usual. While one is on, the log and `crash.log` name it ([MANUAL](MANUAL.md#cheats)).

## Audio

- Audio comes from the translated audio microcode. The test suite checks its level and spectrum; it isn't claimed to be
  bit-exact with the console.

## Untested

- The **park editor**, **split screen in a level** (two players have only been run by a test script: both skaters picked,
  the level loads), **replays** and most **competitions**.
- The **Rumble Pak** on a real controller, and the game's own **Controller Pak manager** (deleting or repairing notes).
- **PAL 50 Hz** (see Game versions).

## Not in this release

Texture packs, mods, and a launcher beyond the first-start window.
