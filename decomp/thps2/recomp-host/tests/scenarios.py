"""Scenario definitions for the THPS2 recomp regression suite (data only; engine in run.py).

Checkpoints describe a screen: the expected RT64 frame size and one or more regions that are
compared with a reference frame recorded locally (build/tests/refs/<name>.png, ROM-derived,
never committed). Regions are fractions of the frame, so they don't depend on the resolution;
each is reduced to a gw x gh luma grid, normalised (zero mean, unit std: fades and brightness
don't matter) and compared by mean absolute difference: 0 = same picture, ~1.1 = unrelated.
`tol` is the largest distance that still counts as a match. `tests/run.py --check-refs`
prints, for each checkpoint, how far the *other* references are (as distance/tol; must stay
well above 1) -- run it after recording or after changing a region.

`record` says how --record captures the reference when none exists: ("frame", N) = at
displayed frame N; ("settle", N) = N displayed frames after the step's input.

Menus are navigated without references: the highlighted entry is gold/red (harness.gold),
the others blue/white, so the cursor row is the strongest gold band inside `y_range`, mapped to
the nearest of `rows` (centres as fractions of the frame height).
"""

# Per-game constants used by run.py (THPS2; a port edits these and the checkpoints below). Game addresses are not
# here: run.py reads them by name from the running version (`peek @gSkater`, `sym Skater_PhysState`;
# versions/host_syms.toml, versions/<class>/data_syms.toml): the pad layer gSControl (20 records of 16 bytes, LOG H3),
# the skater pointer gSkater (CBruce; +Skater_ControlPtr holds gSControl), its physics state word Skater_PhysState
# (0 ground, 1 in air, found by RAM diff around an ollie). The ROM file names are the games.toml `rom_names`.
GAME = dict(
    trick_counters=False,      # THPS2's per-trick counters are not located (LOG H3): the "trick" expectation is not available
    rev0_header=(b"THPS2", b"NTQP"),
)

# Checkpoints whose screen differs on another release, by version id: that release needs its own reference for them, recorded with
# `tools/test.sh --version ID --record` (every other checkpoint uses the first release's picture; games.toml `refs_from`).
OWN_REFS = {
    "thps2_eu": ["main_menu", "wheel_create", "cas_roster"],
}

# name: size, regions [(region (x0, y0, x1, y1), gw, gh, tol)], record
# A region (region, "mask", luma_min, min_frac) is a template match instead: at least min_frac
# of the reference's pixels brighter than luma_min must have the same colour (for HUD text over
# a moving 3D background; harness.mask_score).
# A region (region, "color", (rmin, rmax, gmin, gmax, bmin, bmax), min_frac) counts the pixels inside a colour box (a fixed-colour HUD element
# on a moving background). `regions=[]` = size-only checkpoint (any frame of that size, e.g. a 3D frame; needs no reference).
CHECKPOINTS = {
    # Front end (640x474: 640x480 VI with the first/last lines cropped by the VI timing).
    "notice":         dict(size="640x474", regions=[((0.20, 0.38, 0.80, 0.62), 24, 8, 0.40)], record=("frame", 200),
                           what="EXPANSION PAK FOUND. OK message"),
    "title":          dict(size="640x474", regions=[((0.0, 0.0, 1.0, 1.0), 16, 12, 0.35)], record=("frame", 900),
                           what="logo screen (Tony Hawk's Pro Skater 2, Activision, Neversoft, Edge of Reality) after the legal text"),
    "main_menu": dict(size="640x474", regions=[((0.38, 0.17, 0.62, 0.29), "mask", 200, 0.6)], record=("settle", 90),
                           what="main menu wheel, CAREER MODE on top"),
    "wheel_options": dict(size="640x474", regions=[((0.38, 0.17, 0.62, 0.29), "mask", 200, 0.6)], record=("settle", 60),
                           what="main menu wheel, OPTIONS on top"),
    "wheel_single":   dict(size="640x474", regions=[((0.38, 0.17, 0.62, 0.29), "mask", 200, 0.6)], record=("settle", 60),
                           what="main menu wheel, SINGLE SESSION on top"),
    "wheel_free": dict(size="640x474", regions=[((0.38, 0.17, 0.62, 0.29), "mask", 200, 0.6)], record=("settle", 60),
                           what="main menu wheel, FREE SKATE on top"),
    "wheel_create": dict(size="640x474", regions=[((0.38, 0.17, 0.62, 0.29), "mask", 200, 0.6)], record=("settle", 60),
                           what="main menu wheel, CREATE SKATER on top"),
    "cas_roster": dict(size="640x474", regions=[((0.20, 0.08, 0.80, 0.32), 16, 10, 0.30)], record=("settle", 90),
                           what="CREATE SKATER: CUSTOM SKATER ROSTER (SKATER 1-4, BACK)"),
    "cas_edit": dict(size="640x474", regions=[((0.0, 0.18, 0.52, 0.88), 14, 12, 0.35)], record=("settle", 90),
                           what="CREATE SKATER edit screen: NAME / HOMETOWN / AGE / STYLE / STANCE / WEIGHT panel, the skater turning beside it (a 3D view)"),
    "career_menu": dict(size="640x474", regions=[((0.20, 0.28, 0.80, 0.62), 16, 10, 0.30)], record=("settle", 90),
                           what="career submenu: CONTINUE CAREER (grey) / NEW CAREER / LOAD CAREER"),
    "career_menu_loaded": dict(size="640x474", regions=[((0.20, 0.28, 0.80, 0.62), 16, 10, 0.40)], record=("settle", 90),
                               what="career submenu after loading a career: CONTINUE CAREER enabled"),
    "player_select": dict(size="640x474", regions=[((0.30, 0.55, 0.95, 0.92), 16, 10, 0.30)], record=("settle", 90),
                           what="SELECT PLAYER (Tony Hawk)"),
    "char_menu": dict(size="640x474", regions=[((0.0, 0.62, 0.45, 0.95), 12, 8, 0.30)], record=("settle", 90),
                           what="career player menu: CONTINUE / STYLE / BUY STATS / BUY TRICKS / SKATE SHOP"),
    "level_select": dict(size="640x474", regions=[((0.05, 0.15, 0.62, 0.62), 16, 10, 0.30)], record=("settle", 90),
                           what="LEVEL SELECT: The Hangar"),
    "goals":          dict(size="640x474", regions=[((0.20, 0.0, 0.85, 1.0), 16, 16, 0.40)], record=("settle", 90),
                           what="The Hangar goals sheet, A TO PLAY"),
    "options_menu": dict(size="640x474", regions=[((0.20, 0.15, 0.80, 0.80), 16, 14, 0.30)], record=("settle", 90),
                           what="OPTIONS list: CONTROLLER 1 .. BACK"),
    "pak_menu": dict(size="640x474", regions=[((0.20, 0.38, 0.80, 0.70), 16, 8, 0.30)], record=("settle", 90),
                           what="OPTIONS > CONTROLLER PAK: LOAD DATA / SAVE DATA / LOAD REPLAY / BACK"),
    "enter_name": dict(size="640x474", regions=[((0.05, 0.12, 0.95, 0.50), "mask", 170, 0.7)], record=("settle", 60),
                           what="name entry (letter grid)"),
    "save_ok": dict(size="640x474", regions=[((0.20, 0.455, 0.80, 0.49), "mask", 170, 0.7)], record=("settle", 150),
                           what="SAVE SUCCESSFUL. OK"),
    "load_data_empty": dict(size="640x474", regions=[((0.20, 0.455, 0.80, 0.49), "mask", 170, 0.7)], record=("settle", 120),
                            what="LOAD DATA on a blank pak: no THPS notes"),
    "load_data_list": dict(size="640x474", regions=[((0.44, 0.44, 0.58, 0.56), "mask", 150, 0.7)], record=("settle", 120),
                           what="LOAD DATA: the saved note listed"),
    # In level (320x237). The HUD labels are fixed; everything behind them moves. The mask is the SCORE label's own bright letter pixels (the top
    # three rows of the letters, y 26-30 of 237, x 26-44 of 320, luma >= 170). The first version (x 29-54, y 28-39, luma >= 150) cut the label
    # off below its first rows and included the reference frame's background (sand, luma 130-150 around the 150 limit): ~32 % of the "label" pixels
    # were wall, so the score was 0.68 (ratio 1.58) on every frame whose wall behind the HUD was not that sand colour, 1.0 on the few that were
    # (pause_back / level_grab / pause_resume missed it for 90 s in three macOS gates, 2026-10-14). The new region scores 1.00 on all 71 saved
    # in-level frames and 0.00 on every pause frame (the HUD is hidden in the pause menu).
    "in_level":       dict(size="320x237", regions=[((0.07, 0.10, 0.15, 0.135), "mask", 170, 0.8)], record=("settle", 420),
                           what="in level: SCORE label of the HUD"),
    "pause":          dict(size="320x237", regions=[((0.28, 0.34, 0.72, 0.70), "mask", 200, 0.6)], record=("settle", 30),
                           what="PAUSED menu"),
}

MENUS = {
    "career":  dict(rows=[0.38, 0.466, 0.545], y_range=(0.30, 0.62),
                    items=["CONTINUE CAREER", "NEW CAREER", "LOAD CAREER"]),
    "options": dict(rows=[0.203, 0.264, 0.325, 0.383, 0.444, 0.505, 0.566, 0.627, 0.688, 0.749], y_range=(0.15, 0.80),
                    items=["CONTROLLER 1", "CONTROLLER 2", "SOUND LEVELS", "CONTROLLER PAK", "CHEATS", "HIGH SCORES",
                           "GAP CHECKLIST", "DISPLAY OPTIONS", "CREDITS", "BACK"]),
    "pak":     dict(rows=[0.45, 0.508, 0.569, 0.63], y_range=(0.38, 0.70),
                    items=["LOAD DATA", "SAVE DATA", "LOAD REPLAY", "BACK"]),
    "pause":   dict(rows=[0.386, 0.478, 0.57, 0.66], y_range=(0.30, 0.75),
                    items=["CONTINUE", "RETRY", "CHANGE SOUND LEVELS", "END RUN"]),
}

# Steps (all waits are in displayed frames or checkpoint matches, never wall-clock presses):
#   ("wait_for", cp)                 poll RT64 frames until checkpoint cp matches
#   ("go", BUTTON, from_cp, to_cp)   press BUTTON until to_cp matches (re-pressed only while
#                                    from_cp still matches, i.e. the press was dropped)
#   ("menu", menu, index)            move the cursor (DOWN) until entry `index` is highlighted
#   ("menu_at", menu, index)         assert the cursor is on entry `index` (no input)
#   ("press_after", BUTTON, N)       press exactly N game input polls after the previous press finished
#   ("press", BUTTON)                one press (3 polls held, 3 released)
#   ("menu_name_end",)               name-entry grid: move from the first letter to END
#   ("wait", frames)
#   ("wait_peek", ADDR, VALUE[, S])  frame by frame until the game word at ADDR ("@gRunActive": 1 while a run is played) equals VALUE
#   ("go_watch", BUTTON, FROM_CP, ADDR, VALUE)  press, and wait until the HOST'S GAME THREAD sees the word at ADDR become VALUE (the exact poll)
#   ("press_when", ADDR, GE, BUTTON)  the game thread presses BUTTON at the first poll where the word at ADDR is >= GE (a tick counter; THPS3 cam-43 / cam-219)
#   ("dl", tasks, min_tris)          display-list stats of the next gfx tasks: in-level 3D
#   ("audio", frames, min_rms_dbfs)  RMS of the game's audio output over a window
#   ("fps", seconds, min_median)     median displayed fps from the perf log (warn-only if the
#                                    machine is overloaded: load avg > 2 x CPUs)
#   ("pak_snapshot",) / ("pak_changed",)   hash of <config>/saves/thps2_pak1.mpk before/after
#   ("pak_log", regex)               a host "[thps] pak" log line matching regex was printed
#   ("not_cp", cp)                   the current frame must NOT match cp (negative check)
#   ("max_frame", N)                 the checkpoint just matched came within N displayed frames of boot
#   ("log", regex)                   a host "[thps] skip intro|input|launcher" line matching regex
#   ("fps_overlay", seconds, tol)    Show FPS counter lines agree with the perf log's fps (median, +-tol)
#   ("vpad", "attach")               a virtual SDL game controller (no hardware needed)
#   ("vpress", NAME)                 press + release one of its buttons (SDL names: a, dpdown, y ...)
#   ("bind", INPUT, FIELDS)          replace a binding and save it (controls.cfg), as a user edit would
#   ("file_contains", FILE, regex)   <config>/FILE has a match
#   ("binding_saved", INPUT, B, rx)  the binding was saved (controls.cfg line rx, or controls.json button B)
#   ("audio_max", frames, max_rms)   audio output RMS at most max_rms dBFS (volume setting)
#   ("crash",)                       --control crash: exit 139 and a crash.log naming game code (last step)
#   ("keep_present", NAME)           copy the newest present capture to <out>/NAME.png (UI evidence)
#   ("json_value", FILE, KEY, VALUE) <config>/FILE (recompui settings JSON) has KEY = VALUE
#   ("loadrom", "rom"|"rev0", regex) launcher Load ROM (--control loadrom) with the suite's ROM or a
#                                    synthetic v1.0 header; the host log matches regex
#   ("pad_records", INPUT, [ids])    while INPUT ("vpad:NAME" or N64 buttons) is held, exactly these
#                                    records of the game's PlayStation-style pad layer are pressed
#                                    (0 grind, 1 flip, 2 grab, 3 ollie, ...; run.py)
#   ("skate", INPUTS, "air")         vpad inputs on the ground; the skater gets airborne (CBruce via the skater
#                                    pointer @gSkater; no trick counters located for THPS2)
#   ("edges", N, max)                border bands of the next N presented frames change by <= max
#   ("present_wide", "WxH", max)     newest present capture (session `present_every`) is WxH and at
#                                    most `max` of the bands outside the central 4:3 is unrendered
#   ("hfr_motion", SEC, STICK, checks) / ("hfr_cut",) / ("latency", "A/B", N, MAX_MS)
#                                    high frame rate + input latency (tests/hfr_steps.py)

from hfr_steps import ids_phases as IDS_PHASES, ids_clip as IDS_CLIP  # noqa: E402

# Inside a controls screen the OPTIONS list is not shown (no reference frame of the screens themselves; THPS1's options-controls).
IN_SCREEN = [("wait", 40), ("shot", "in_controls_screen"), ("not_cp", "options_menu")]

BOOT_TO_MENU = [
    ("wait_for", "title"),
    ("go", "START", "title", "main_menu"),
]

# main_menu (wheel, CAREER MODE on top) -> career submenu -> NEW CAREER -> player -> player menu -> level select -> goals
CAREER_TO_GOALS = [
    ("go", "A", "main_menu", "career_menu"),
    ("menu_at", "career", 1),                    # no career yet: cursor on NEW CAREER
    ("go", "A", "career_menu", "player_select"),
    ("go", "A", "player_select", "char_menu"),
    ("go", "A", "char_menu", "level_select"),
    ("go", "A", "level_select", "goals"),
]

# Sessions = one host instance each; scenarios in a session run in order on the same instance
# (a failure skips the rest of that session). `fresh_pak` starts from a blank Controller Pak.
# feel-*: FEEL_TRICKS=1 = ollies + flip tricks + turns (bails included) instead of the plain forward / turn route
_FEEL_TRICKS = [x for k in range(6) for x in [
    ("wait", 20), ("ctl", "vpad button a 1"), ("wait", 8), ("ctl", "vpad button a 0"), ("wait", 4),
    ("ctl", "vpad axis leftx " + ("-32000" if k % 2 else "32000")), ("ctl", "vpad button x 1"), ("wait", 6), ("ctl", "vpad button x 0"),
    ("wait", 14), ("ctl", "vpad axis leftx 0")]]

# 2 PLAYER > TRICK ATTACK with two virtual pads (pad 1 = port 1, pad 2 = port 2) up to the split-screen run; then each pad reaches its own port.
_TWO_PADS_TO_LEVEL = [
    *BOOT_TO_MENU,
    ("vpad", "attach"), ("vpad2", "attach"),
    ("vpress", "leftshoulder"), ("vpress2", "leftshoulder"),           # pad 1 = port 1, pad 2 = port 2
    ("log_n", r"Virtual Controller takes port 2", 1),
    ("wait", 90), *[("vpress", "dpright"), ("wait", 40)] * 3,
    *[x for _ in range(4) for x in (("vpress", "a"), ("wait", 150))],   # the wheel's 2 PLAYER, TRICK ATTACK, PLAYER 1 select, its CONTINUE
    *[x for _ in range(2) for x in (("vpress2", "a"), ("wait", 150))],  # PLAYER 2 select, its CONTINUE: port 2 (pad 1's A does nothing there)
    ("vpress", "a"), ("wait", 60), ("vpress2", "a"), ("wait", 150),   # HANDICAP: each player accepts his own ("WAITING FOR OTHER PLAYER")
    *[x for _ in range(3) for x in (("vpress", "a"), ("wait", 150))],   # LEVEL SELECT, rules, SELECT TIME
    ("wait_peek", "@gRunActive", 1, 60),
]
_TWO_PADS_PORTS = [
    ("ctl", "vpad2 button leftshoulder 1"), ("wait", 8),
    ("ctl_match", "inputstate", r"last=0x0000 last2=0x0020$"),        # pad 2 reaches port 2 only
    ("ctl", "vpad2 button leftshoulder 0"),
    ("ctl", "vpad button rightshoulder 1"), ("wait", 8),
    ("ctl_match", "inputstate", r"last=0x0010 last2=0x0000$"),        # pad 1 port 1 only
    ("ctl", "vpad button rightshoulder 0"),
]

SESSIONS = [
    dict(name="frontend", config="suite-config", fresh_pak=True, wav=True, scenarios=[
        ("boot_title", "boot: Expansion Pak notice, legal text, then the logo/title screen (overlay t2_intro)", [
            ("wait_for", "title"),
            ("edges", 20, 4.0),
        ]),
        ("main_menu",  "logos -> START -> main menu wheel (overlays t2_loadcareer / t2_menuwheel)", [("go", "START", "title", "main_menu")]),
        ("career_level", "CAREER MODE -> NEW CAREER -> player -> The Hangar loaded, HUD + 3D", [
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("dl", 10, 500),
        ]),
        ("level_audio", "in-level audio is not silent", [("wait", 60), ("audio", 150, -40.0)]),
        ("level_fps",   "in-level median fps >= 28", [("fps", 10, 28.0)]),
        # THPS2's pad layer (LOG H3): C-up/left/right/down = records 0/1/2/3 (grind/flip/grab/ollie), and
        # unlike THPS1 N64 A = ollie (3) and N64 B = flip (1) in the skating code too. thps-xbox: south
        # = A + C-down (ollie), west = C-left (flip), east = C-right (grab; its N64 B is dropped while the skater is
        # under control, src/run_state.cpp; in every other screen C-right is dropped and B = back stays), north = C-up (grind).
        ("level_controls", "default pad bindings reach the game's trick buttons (A/B are ollie/flip too)", [
            ("vpad", "attach"),
            ("pad_records", "A", [3]),            # N64 A: ollie (also menu accept)
            ("pad_records", "B", [1]),            # N64 B: flip (also menu back)
            ("pad_records", "CD", [3]),
            ("pad_records", "CL", [1]),
            ("pad_records", "CR", [2]),
            ("pad_records", "CU", [0]),
            ("pad_records", "vpad:a", [3]),       # south (Xbox A) = A + C-down -> ollie
            ("pad_records", "vpad:x", [1]),       # west (Xbox X) = C-left -> flip
            ("pad_records", "vpad:b", [2]),       # east (Xbox B) = C-right -> grab ONLY (B dropped in 3D, no flip)
            ("pad_records", "vpad:y", [0]),       # north (Xbox Y) = C-up -> grind
        ]),
        ("level_ollie", "Xbox A held and released: the skater ollies (in air)", [
            ("skate", [("vpad", "a", 1), ("wait", 10), ("vpad", "a", 0)], "air"),
        ]),
        ("level_grab", "Xbox A, then B + right and Y in the air: the level keeps running", [
            ("skate", [("vpad", "a", 1), ("wait", 10), ("vpad", "a", 0), ("wait", 3),
                       ("axis", "leftx", 32767), ("vpad", "b", 1), ("wait", 6), ("vpad", "b", 0), ("vpad", "y", 1), ("wait", 4),
                       ("vpad", "y", 0), ("axis", "leftx", 0)], "air"),
            ("wait", 30),
            ("wait_for", "in_level"),
            ("wait_peek", "@gRunActive", 1),     # the game's own flag: a level run is being played
        ]),
        ("border_stable", "pause menu: the border bands of the presented frames don't flicker", [
            ("go", "START", "in_level", "pause"),
            ("wait", 20),
            ("edges", 45, 4.0),
        ]),
        # The pause menu draws the 3D level behind it, and the game says "B TO GO BACK". Xbox B (east) is N64 B + C-right; the host used to
        # drop B whenever a 3D view was drawn, so back never arrived here (and in Create-a-Skater, the end-of-run and name-entry screens...).
        # Now B is dropped only while the skater is under control (src/run_state.cpp), and in every other screen C-right is dropped instead.
        ("pause_sub_back", "pause menu > CHANGE SOUND LEVELS: Xbox B (east) goes back to the pause menu (a 3D view is drawn behind it)", [
            ("menu", "pause", 2),
            ("press", "A"),
            ("wait", 40),
            ("not_cp", "pause"),
            ("vpress", "b"),
            ("wait", 30),
            ("menu_at", "pause", 2),             # back on the pause list with the cursor where it was (the sound sub-menu's own highlight is at the top)
        ]),
        ("pause_back", "pause menu: Xbox B (east) goes back = resumes the level", [
            ("vpress", "b"),
            ("wait", 30),
            ("wait_for", "in_level"),
            ("wait_peek", "@gRunActive", 1),     # resumed = the run flag is back (the HUD alone is only what the picture shows)
            ("not_cp", "pause"),
        ]),
        ("level_b_after_resume", "after the resume the skater is under control again: east sends C-right only (grab, no flip)", [
            ("pad_records", "vpad:b", [2]),
        ]),
        ("pause_resume", "pause menu: START resumes the level", [
            ("go", "START", "in_level", "pause"),
            ("press", "START"), ("wait", 30), ("wait_for", "in_level"), ("wait_peek", "@gRunActive", 1), ("not_cp", "pause"),
        ]),
    ]),
    # Create-a-Skater: the edit screen draws a 3D skater (so a "3D view is drawn" test counted it as skating), and the roster uses C-right = LOAD.
    # Xbox B (east) = N64 B + C-right must go back in both: before the fix B was dropped on the edit screen, and on the roster C-right opened
    # the LOAD dialog (the "no career saves found" box) instead of the back.
    dict(name="cas", config="cas-config", fresh_pak=True, wav=False, args=["--skip-intro", "--hidden"],
         fresh_files=["controls.cfg", "controls.json", "general.cfg"], scenarios=[
        ("cas_back", "CREATE SKATER: Xbox B (east) goes back from the 3D edit screen to the roster and from the roster to the wheel", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            ("wait", 90),                         # the wheel ignores input while it animates in
            ("press", "RIGHT"), ("wait", 30), ("press", "RIGHT"), ("wait", 30), ("press", "RIGHT"), ("wait", 30), ("press", "RIGHT"), ("wait", 30),
            ("wait_for", "wheel_create"),
            ("go", "A", "wheel_create", "cas_roster"),
            ("vpad", "attach"),
            ("vpress", "rightstick"),             # claims port 1 (a virtual controller takes a port on its first press)
            ("go", "A", "cas_roster", "cas_edit"),
            ("vpress", "b"),
            ("wait_for", "cas_roster"),
            ("vpress", "b"),
            ("wait_for", "wheel_create"),
        ]),
        ("cas_scripted_b", "a scripted B (and the n64 preset's west button, which is plain N64 B) still goes back from the 3D edit screen", [
            ("go", "A", "wheel_create", "cas_roster"),
            ("go", "A", "cas_roster", "cas_edit"),
            ("press", "B"),
            ("wait_for", "cas_roster"),
            ("ctl", "preset n64"),
            ("go", "A", "cas_roster", "cas_edit"),
            ("vpress", "x"),
            ("wait_for", "cas_roster"),
            ("ctl", "preset thps-xbox"),
        ]),
    ]),
    # Widescreen: the RDRAM frames the checkpoints compare stay native 4:3, so the 4:3 references apply;
    # the present capture checks the wide picture. Own config dir.
    dict(name="widescreen", config="ws-config", fresh_pak=True, wav=False, present_every=30,
         args=["--aspect", "16:9", "--window", "1280x720", "--res-scale", "2", "--msaa", "4", "--hidden", "--skip-intro"], scenarios=[
        ("ws_menu", "16:9: boot to the main menu (native frames unchanged)", [*BOOT_TO_MENU]),
        ("ws_level", "16:9: the Hangar fills the wide frame (present capture), 30 fps", [
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("dl", 10, 500),
            ("wait", 60),
            ("present_wide", "1280x720", 0.15),
            ("fps", 10, 28.0),
        ]),
    ]),
    dict(name="pak", config="pak-config", fresh_pak=True, wav=False, args=["--skip-intro", "--hidden"], scenarios=[
        ("pak_empty", "fresh pak: OPTIONS > CONTROLLER PAK > LOAD DATA finds no notes", [
            *BOOT_TO_MENU,
            ("go", "LEFT", "main_menu", "wheel_options"),
            ("go", "A", "wheel_options", "options_menu"),
            ("menu", "options", 3),
            ("go", "A", "options_menu", "pak_menu"),
            ("menu_at", "pak", 0),
            ("go", "A", "pak_menu", "load_data_empty"),
            ("go", "B", "load_data_empty", "options_menu"),   # the dialog's B returns to the OPTIONS list (cursor on CONTROLLER PAK)
            ("go", "A", "options_menu", "pak_menu"),
        ]),
        ("pak_save", "OPTIONS > CONTROLLER PAK > SAVE DATA > name 'A' writes a note (.mpk changes)", [
            ("pak_snapshot",),
            ("menu", "pak", 1),
            ("go", "A", "pak_menu", "enter_name"),
            ("press", "A"),                      # letter A
            ("menu_name_end",),
            ("go", "A", "enter_name", "save_ok"),
            ("pak_log", r"pak 1: wrote \d+ bytes"),
            ("pak_changed",),
            ("press", "A"),                      # dismiss the dialog (back on the pak menu, cursor on SAVE DATA)
            ("wait", 30),
        ]),
    ]),
    dict(name="pak-reload", config="pak-config", fresh_pak=False, wav=False, needs=["pak"], args=["--skip-intro", "--hidden"], scenarios=[
        ("pak_list", "fresh run on the saved pak: LOAD DATA lists the note", [
            *BOOT_TO_MENU,
            ("go", "LEFT", "main_menu", "wheel_options"),
            ("go", "A", "wheel_options", "options_menu"),
            ("menu", "options", 3),
            ("go", "A", "options_menu", "pak_menu"),
            ("go", "A", "pak_menu", "load_data_list"),
            ("not_cp", "load_data_empty"),
        ]),
        ("pak_load", "load the note: host reads it back from the pak", [
            ("press", "A"),
            ("pak_log", r"pak 1: read \d+ bytes at 0 of note 0"),
        ]),
    ]),
    # OPTIONS > CONTROLLER 1 / CONTROLLER 2 (the game's controls screens; THPS1's soft lock was its PLAYER 2 CONTROLS, LOG "PLAYER 2 CONTROLS").
    # THPS2's CONTROLLER 2 opens only for port 2's A (port 1's A does nothing on that row, also with two pads), and inside it port 1's
    # B leaves as well as port 2's: so it never locked, but with one pad it could not be opened. The host's p2_menu_mirror (game.toml;
    # port 2 = port 1 in menus while no second pad is attached, input.cpp) opens it. Inside a controls screen the OPTIONS list is not
    # shown (not_cp options_menu); leaving must bring OPTIONS back. Leaving CONTROLLER 2 keeps the cursor on its row.
    dict(name="options-controls", config="optctl-config", fresh_pak=True, wav=False, args=["--skip-intro", "--hidden", "--keyboard"], scenarios=[
        ("ctlscr_p1_pad", "pad: A enters CONTROLLER 1, B (east) leaves", [
            *BOOT_TO_MENU,
            ("go", "LEFT", "main_menu", "wheel_options"),
            ("go", "A", "wheel_options", "options_menu"),
            ("menu_at", "options", 0),
            ("vpad", "attach"), ("vpress", "leftshoulder"),              # the first press claims port 1 (a button that does nothing here)
            ("vpress", "a"), *IN_SCREEN,
            ("vpress", "b"), ("wait_for", "options_menu"),
            ("menu_at", "options", 0),
        ]),
        ("ctlscr_p2_pad", "ONE pad: A opens CONTROLLER 2 (it waited for port 2's A: did nothing), B leaves", [
            ("wait", 30), ("vpress", "dpdown"), ("menu_at", "options", 1),
            ("vpress", "a"), *IN_SCREEN,
            ("vpress", "b"), ("wait_for", "options_menu"),
            ("menu_at", "options", 1),
        ]),
        ("ctlscr_p2_kbd", "keyboard only: Space opens CONTROLLER 2, D leaves", [
            ("wait", 30), ("ctl", "key Space"), *IN_SCREEN,
            ("ctl", "key D"), ("wait_for", "options_menu"),
            ("menu_at", "options", 1),
        ]),
        ("ctlscr_p2_two_pads", "TWO pads: pad 1's A does not open CONTROLLER 2 (no mirror), pad 2's A does and its B leaves; "
                               "pad 2 unplugged inside: pad 1's B leaves", [
            ("vpad2", "attach"), ("vpress2", "leftshoulder"),
            ("log_n", r"Virtual Controller takes port 2", 1),
            ("wait", 30), ("vpress", "a"), ("wait", 40), ("wait_for", "options_menu"), ("menu_at", "options", 1),
            ("vpress2", "a"), *IN_SCREEN,
            ("vpress2", "b"), ("wait_for", "options_menu"),
            ("wait", 30), ("vpress2", "a"), *IN_SCREEN,
            ("vpad2", "detach"), ("wait", 20),
            ("vpress", "b"), ("wait_for", "options_menu"),
        ]),
    ]),
    # 2 PLAYER (hand play lead 2026-10-15): after PLAYER 1 has picked a skater, PLAYER 2 CHOOSE SKATER reads only port 2, so with ONE
    # pad (or the keyboard) neither A nor B did anything there: a soft lock (quit the app). With p2_menu_mirror port 2 carries port
    # 1's input in menus (the run flag gRunActive is 0: THPS2's select screens draw the skater in 3D, so "no 3D drawn" cannot be the
    # rule), and stops in the level (split screen, the run being played): there port 2 is empty again.
    # Screens after the 2 PLAYER GAMES list (one A each): PLAYER 1 select, its CONTINUE, PLAYER 2 select, its CONTINUE, HANDICAP,
    # LEVEL SELECT, the mode's rules, SELECT TIME, then the level.
    dict(name="two-players", config="two-players-config", fresh_pak=True, wav=False, args=["--skip-intro", "--hidden"], scenarios=[
        ("two_p_one_pad", "ONE pad: 2 PLAYER > TRICK ATTACK, both skaters picked with it, the split-screen level loads; there port 2 is empty", [
            *BOOT_TO_MENU,
            ("vpad", "attach"), ("vpress", "leftshoulder"),
            ("wait", 90),                                                  # the wheel menu ignores input while it animates in
            *[("vpress", "dpright"), ("wait", 40)] * 3,                   # the wheel: 2 PLAYER on top
            *[x for _ in range(10) for x in (("vpress", "a"), ("wait", 150))],
            ("wait_peek", "@gRunActive", 1, 60),
            ("shot", "two_p_one_pad_level"),
            ("ctl", "vpad button leftshoulder 1"), ("wait", 8),
            ("ctl_match", "inputstate", r"in_control=1 .*last=0x0020 last2=0x0000$"),   # port 1 has L, port 2 nothing (no mirror in a run)
            ("ctl", "vpad button leftshoulder 0"),
        ]),
    ]),
    dict(name="two-players-pads", config="two-players-pads-config", fresh_pak=True, wav=False, args=["--skip-intro", "--hidden"], scenarios=[
        ("two_p_two_pads", "TWO pads: each picks its own skater, the split-screen level loads, each pad reaches its own port", [
            *_TWO_PADS_TO_LEVEL,
            *_TWO_PADS_PORTS,
        ]),
    ]),
    # QOL features: Skip Intro, Show FPS, remappable bindings with a virtual controller,
    # then the crash log (the host dies, so it is the last step). Fresh settings files each run.
    dict(name="qol", config="qol-config", fresh_pak=True, wav=False,
         fresh_files=["controls.cfg", "general.cfg", "crash.log", "controls.json", "general.json", "graphics.json", "sound.json"],
         args=["--skip-intro", "--show-fps", "--hidden"], scenarios=[
        ("skip_intro", "Skip Intro: boot to the logo/title screen in < 200 frames, no legal text (was ~1100)", [
            ("wait_for", "title"),
            ("max_frame", 200),
            ("log", r"skip intro: pressing B on the Expansion Pak notice"),
            ("log", r"skip intro: legal screen skipped"),
            ("go", "START", "title", "main_menu"),
        ]),
        ("fps_counter", "Show FPS: counter lines match the perf log", [("fps_overlay", 5, 2.0)]),
        ("vpad_bindings", "virtual controller turns the menu wheel; rebinding D-pad Right to Y works and is saved", [
            ("vpad", "attach"),
            ("vpress", "dpleft"),
            ("log", r"Virtual Controller takes port 1"),
            ("wait_for", "wheel_options"),
            ("bind", "dpad_right", "button:y"),
            ("binding_saved", "dpad_right", 3, r"(?m)^dpad_right = button:y$"),   # SDL button 3 = Y
            ("vpress", "y"),
            ("wait_for", "main_menu"),
            ("vpress", "dpright"),            # no longer bound: the wheel stays
            ("wait", 30),
            ("wait_for", "main_menu"),
        ]),
        ("crash_log", "a crash writes crash.log with the game function names", [("crash",)]),
    ]),
    dict(name="qol-reload", config="qol-config", fresh_pak=False, wav=False, needs=["qol"],
         args=["--skip-intro", "--volume", "0", "--hidden"], scenarios=[
        ("bindings_persist", "controls.cfg from the last run: Y is D-pad Right", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            ("vpad", "attach"),
            ("wait", 90),                    # the wheel menu ignores input while it animates in
            ("vpress", "y"),                 # Y = D-pad Right: the wheel turns away from CAREER MODE
            ("wait_for", "wheel_single"),
        ]),
        ("volume_zero", "--volume 0: the audio output is silent", [("audio_max", 90, -90.0)]),
    ]),
    # Widescreen must not change the game: the same paused frame at 4:3 (records the reference) and
    # at 21:9 (compares). The 21:9 present capture must also fill the side bands.
    dict(name="cam-43", config="cam43-config", fresh_pak=True, wav=False, args=["--skip-intro", "--hidden", "--aspect", "original", "--window", "960x720"], scenarios=[
        ("cam_ref_43", "4:3 (960x720): the Hangar paused 200 polls after the start; still border bands", [
            ("wait_for", "title"), ("go", "START", "title", "main_menu"), *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("press_after", "START", 200), ("wait", 30), ("wait_for", "pause"),
            ("edges", 45, 4.0),
        ]),
    ]),
    # The THPS1 suite also compared a paused native frame at 4:3 and 21:9 (camera unchanged by widescreen). In
    # THPS2 the number of game frames between A and the first level frame varies by a few frames from run
    # to run (threaded loading), so that exact-frame comparison fails (distance 0.35 for a 3-5 frame
    # offset): the 21:9 session only checks that the 3D fills the wide frame.
    dict(name="cam-219", config="cam219-config", fresh_pak=True, wav=False, present_every=15,
         args=["--skip-intro", "--hidden", "--aspect", "21:9", "--window", "1680x720", "--res-scale", "2"], scenarios=[
        ("wide_219", "21:9: the Hangar fills the side bands (present capture)", [
            ("wait_for", "title"), ("go", "START", "title", "main_menu"), *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("wait", 60),
            ("present_wide", "1680x720", 0.10),
        ]),
    ]),
    # Frontend build only (THPS2_BINARY=build/cmake-ui/thps2_recomp; skipped otherwise): the
    # launcher and settings menu, driven with the virtual controller. A setting changed in the menu
    # is saved, and a new process starts the game from the launcher with it.
    dict(name="ui", config="ui-config", fresh_pak=True, wav=False, requires="frontend", present_every=6,
         fresh_files=["controls.json", "general.json", "graphics.json", "sound.json"],
         args=["--launcher", "--hidden"], scenarios=[
        ("ui_launcher", "launcher shows Start Game (ROM stored)", [
            ("log", r"launcher ready \(ROM stored: Start Game\)"),
            ("vpad", "attach"),
            ("wait", 60),
            ("keep_present", "ui_launcher"),
        ]),
        ("ui_settings", "Settings: General Skip Intro + Show FPS ON, Graphics Aspect Ratio ORIGINAL + Apply, Sound volume 97; saved", [
            ("vpress", "dpdown"), ("vpress", "dpdown"), ("vpress", "a"), ("wait", 60),          # launcher: Settings
            ("vpress", "dpdown"), ("vpress", "dpdown"), ("vpress", "dpdown"), ("vpress", "dpdown"),
            ("vpress", "dpright"), ("vpress", "a"),                                             # Skip Intro: ON
            ("vpress", "dpdown"), ("vpress", "dpright"), ("vpress", "a"), ("wait", 30),         # Show FPS: ON
            ("keep_present", "ui_general_skip_intro_on"),
            ("log", r"settings: skip_intro=1 show_fps=1"),
            ("vpress", "rightshoulder"), ("wait", 30), ("keep_present", "ui_tab_controls"),
            ("vpress", "rightshoulder"), ("wait", 30), ("keep_present", "ui_tab_graphics"),
            ("vpress", "dpdown"), ("vpress", "dpdown"), ("vpress", "dpleft"), ("vpress", "a"),   # Aspect Ratio: ORIGINAL
            ("vpress", "dpdown"), ("vpress", "dpdown"), ("vpress", "dpdown"), ("vpress", "dpdown"),
            ("vpress", "a"), ("wait", 30),                                                      # Apply
            ("keep_present", "ui_graphics_applied"),
            ("log", r"gfx: aspect=original"),
            ("vpress", "rightshoulder"), ("wait", 30),
            ("vpress", "dpdown"), ("vpress", "dpleft"), ("vpress", "dpleft"), ("vpress", "dpleft"),  # Main Volume 100 -> 97
            ("keep_present", "ui_tab_sound"),
            ("log", r"settings: .* volume=97"),
            ("vpress", "back"), ("wait", 60),
            ("json_value", "general.json", "thps_skip_intro", "On"),
            ("json_value", "general.json", "thps_show_fps", "On"),
            ("json_value", "graphics.json", "ar_option", "Original"),
            ("json_value", "sound.json", "main_volume", 97),
        ]),
    ]),
    # Frontend build, no ROM stored: the launcher offers Load ROM; a v1.0 header is refused with
    # our wording (an in-UI prompt), the real ROM is accepted and the entry becomes Start Game.
    dict(name="ui-norom", config="ui-norom-config", fresh_pak=True, wav=False, requires="frontend", present_every=6,
         no_rom=True, fresh_files=["thps2.n64.us.z64", "general.json", "graphics.json", "sound.json", "controls.json"],
         args=["--launcher", "--hidden"], scenarios=[
        ("ui_load_rom", "no ROM: Load ROM; PAL-code header refused (THPS2 USA wording); the ROM accepted -> Start Game", [
            ("log", r"launcher ready \(no ROM yet: Load ROM\)"),
            ("vpad", "attach"), ("wait", 60),
            ("keep_present", "ui_launcher_no_rom"),
            ("loadrom", "rev0", r"game code NTQP"), ("wait", 30),
            ("keep_present", "ui_rom_rejected"),
            ("vpress", "a"), ("wait", 30),
            ("loadrom", "rom", r"launcher: ROM stored, Start Game"), ("wait", 30),
            ("keep_present", "ui_launcher_rom_ok"),
        ]),
    ]),
    dict(name="ui-start", config="ui-config", fresh_pak=False, wav=False, requires="frontend", present_every=6,
         needs=["ui"], args=["--launcher", "--hidden"], scenarios=[
        ("ui_start_game", "new process: settings loaded (Skip Intro, Show FPS, 4:3, volume 97); Start Game -> title; FPS overlay; in-game menu", [
            ("log", r"gfx: aspect=original"),
            ("log", r"launcher ready"),
            ("vpad", "attach"),
            ("wait", 60),
            ("vpress", "dpdown"), ("vpress", "dpup"), ("vpress", "a"),
            ("wait_for", "title"),
            ("log", r"skip intro: legal screen skipped"),
            ("fps_overlay", 3, 2.0),
            ("keep_present", "ui_title_fps"),
            ("vpress", "back"), ("wait", 45),
            ("keep_present", "ui_ingame_menu"),
        ]),
    ]),
    # Matrix-group IDs (src/interp_ids.cpp): pairing statistics + idsdump (RT64's verdict per world transform joined with the display-list walk).
    dict(name="idsprobe", config="idsprobe-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro", "--hidden", "--refresh", "60", "--present-size", "480x360"], scenarios=[
        ("ids_probe", "evidence: pairing statistics standing / skating / turning / ollie, then idsdump", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            ("ctl", "idsscan 1"),
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            *IDS_PHASES(40, True),
        ]),
    ]),
    # Performance of the matrix IDs (docs/interpolation-ids.md, "Performance"): VISIBLE window, no capture; IDs off / on interleaved, a present-dump block and an idsstat block
    # for the cost of those debug modes, and a --refresh original baseline in the second session.
    dict(name="idsbench", config="idsbench-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro"] + __import__("os").environ.get("THPS_BENCH_ARGS", "").split(), scenarios=[
        ("ids_bench", "performance: fps, frame-time percentiles, ID walk cost; IDs off/on interleaved (notes)", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("vpad", "attach"), ("wait", 30),
            ("bench", 12, "keep"),                       # warm-up
            ("bench", 20, "off"), ("bench", 20, "on"), ("bench", 20, "naive"), ("bench", 20, "off"), ("bench", 20, "on"), ("bench", 20, "naive"),
            ("bench", 20, "off"), ("bench", 20, "on"), ("bench", 20, "naive"),
        ]),
    ]),
    dict(name="idsbench-orig", config="idsbench-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro", "--refresh", "original"] + __import__("os").environ.get("THPS_BENCH_ARGS", "").split(), scenarios=[
        ("ids_bench_orig", "performance baseline: --refresh original (30 fps, no interpolation)", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("vpad", "attach"), ("wait", 30),
            ("bench", 12, "keep"),
            ("bench", 20, "keep"), ("bench", 20, "keep"), ("bench", 20, "keep"),
        ]),
    ]),
    dict(name="idsclip", config="idsclip-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro", "--hidden", "--refresh", "60", "--present-size", "480x360"], scenarios=[
        ("ids_clip", "evidence: every composited frame of ~8 s of skating (THPS_IDS=1: IDs on), into build/ids/clip", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            *IDS_CLIP(),
        ]),
    ]),
    # The one-frame "hole" (src/interpolation.cpp "projection kinds"): skating off the Hangar start, the camera catches up fast and RT64
    # paired the camera scene with the skater's planar-shadow scene for one in-between frame (skater and half the world gone). Before the
    # fix 11 of 12 captured runs had one or two such frames (--hfr-proj-ids 0 reproduces it); every composited frame of 3 s is checked.
    dict(name="hole", config="hole-config", fresh_pak=True, wav=False,
         args=["--refresh", "60", "--skip-intro", "--hidden", "--present-size", "480x360"], scenarios=[
        ("hfr_hole", "60 Hz: no presented frame loses the skater / half the world (camera paired with the shadow scene)", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("wait", 30),
            ("hfr_hole", 3.0),
        ]),
        # The view-projection split (src/interpolation.cpp): RT64 split the combined camera matrix with the depth scale from the x row
        # alone; looking down the Hangar start ramp (camera along the world z axis) that row is ~0: wrong depth range or a NaN split
        # (camera filed as orthographic: no pairing, a 30 Hz step) on ~30 % of the loads. The host re-splits every camera load.
        ("vp_split", "every camera load re-split by the host on the Hangar start route, where RT64's own split fails", [
            ("press", "START"), ("wait", 30), ("menu", "pause", 1), ("go", "A", "pause", "in_level", 90), ("wait", 30),
            ("vp_split", 3.0),
        ]),
    ]),
    # Exploration (play-test "feel" findings): every composited frame of ~6 s skating off the start of the Hangar / School II, into
    # build/feel/<session>/ (ROM-derived: local). FEEL_ARGS adds host args (e.g. "--aspect original --refresh original").
    *[dict(name="feel-" + lv, config="feel-config", fresh_pak=True, wav=False, optin=True,
           args=["--refresh", "60", "--skip-intro", "--hidden", "--present-size", "480x360", "--unlock-levels"] + __import__("os").environ.get("FEEL_ARGS", "").split(),
           scenarios=[
        ("feel_" + lv, "evidence: every composited frame of the first seconds of " + lv, [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            *CAREER_TO_GOALS[:-1],
            *([("press", "RIGHT"), ("wait", 45)] if lv == "school" else []),
            ("press", "A"), ("wait", 120), ("shot", "goals_" + lv),
            ("go", "A", "goals" if lv == "hangar" else "level_select", "in_level", 90),
            ("wait", 30), ("vpad", "attach"),
            ("ctl", "projids"), ("ctl", "hfr"), ("ctl", "vpsplit"),
            ("ctl", "pcap 1 build/feel/" + lv), ("ctl", "vpad axis lefty -32000"),
            *(_FEEL_TRICKS if __import__("os").environ.get("FEEL_TRICKS") else [
              ("wait", 60), ("ctl", "vpad axis leftx -32000"), ("wait", 45), ("ctl", "vpad axis leftx 32000"), ("wait", 90),
              ("ctl", "vpad axis leftx 0"), ("wait", 45)]),
            ("ctl", "pcap 0"), ("ctl", "vpad axis lefty 0"),
            ("ctl", "projids"), ("ctl", "hfr"), ("ctl", "vpsplit"),
        ]),
    ]) for lv in ("hangar", "school")],
    # High frame rate: 60 Hz frame interpolation in the Hangar (every composited frame captured small),
    # and input latency on the main menu. Explicit --refresh 60.
    dict(name="hfr", config="hfr-config", fresh_pak=True, wav=False,
         args=["--refresh", "60", "--skip-intro", "--hidden", "--present-size", "480x360"], scenarios=[
        ("input_latency", "main menu: press -> first changed presented frame (median of 6, <= 100 ms)", [
            ("wait_for", "title"),
            ("go", "START", "title", "main_menu"),
            ("latency", "RIGHT/LEFT", 6, 100.0),
        ]),
        ("hfr_motion", "60 Hz interpolation: every refresh shows a new, evenly spaced frame while skating", [
            *CAREER_TO_GOALS,
            ("go", "A", "goals", "in_level", 90),
            ("wait", 30),
            ("hfr_motion", 4.0, "SUP", dict(fm60=0.9, alt=0.3, interp=0.9, paired=0.88, dropped=0.05)),
            ("fps", 5, 28.0),
        ]),
    ]),
]

# HUD placement (src/hud_anchor.cpp): regression sessions (hud = the default, hud-original, hud-43) and optin present captures (hud-<orig169|orig219|edge169|edge219|clamp219>,
# hud-dbg; run by name): the sessions are built in the shared tests/hud_sessions.py from this game's navigation steps.
from hud_sessions import hud_sessions  # noqa: E402
SESSIONS += hud_sessions([*CAREER_TO_GOALS, ("go", "A", "goals", "in_level", 90)], pause_menu='pause', end_run=3, boot=BOOT_TO_MENU)

# Cheats (test aids, game/cheats.cpp; the game's own cheats through the Cheat_IsOn hook): exploration (opt-in, CS_ARGS = cheat flags).
import os as _os
_CS_TRY = [("axis", "lefty", -32767), ("vpad", "a", 1), ("wait", 8), ("vpad", "a", 0), ("wait", 2), ("axis", "leftx", 32767), ("vpad", "x", 1),
           ("wait", 4), ("vpad", "x", 0), ("axis", "leftx", 0), ("vpad", "y", 1), ("wait", 12), ("vpad", "y", 0)]
SESSIONS += [
    dict(name="cheats-explore", config="cheats-explore-config", fresh_files=["cheats.cfg"], fresh_pak=True, wav=False, optin=True, args=["--skip-intro"] + _os.environ.get("CS_ARGS", "").split(), scenarios=[
        ("cheats_explore", "exploration: first level, forward + ollie + flip + grind presses; skater state / rail balance / time scale samples", [
            *BOOT_TO_MENU, *CAREER_TO_GOALS, ("go", "A", "goals", "in_level", 90), ("wait", 30),
            ("vpad", "attach"),
            ("skater_watch", 80, _CS_TRY, ["Skater_PhysState", "Skater_RailBalance", "@gTimeScale"]),
            ("ctl", "vpad axis lefty 0"),
            ("go", "START", "in_level", "pause"), ("wait", 20), ("shot", "pause"),
        ]),
    ]),
]

from cheat_sessions import cheat_sessions  # noqa: E402
SESSIONS += cheat_sessions(BOOT_TO_MENU, [*CAREER_TO_GOALS, ("go", "A", "goals", "in_level", 90)], [
    ("go", "LEFT", "main_menu", "wheel_options"), ("go", "A", "wheel_options", "options_menu"),
    ("menu", "options", 3), ("go", "A", "options_menu", "pak_menu"),
    ("menu", "pak", 1), ("go", "A", "pak_menu", "enter_name"), ("press", "A"), ("menu_name_end",),
    ("go", "A", "enter_name", "save_ok"), ("pak_log", r"pak 1: wrote \d+ bytes"),
], _CS_TRY)

# The in-game settings menu (THPS_MENU builds; skipped otherwise): tests/menu_session.py in the shared host.
from menu_session import MENU_SESSIONS  # noqa: E402
SESSIONS += MENU_SESSIONS

# Draw distance (2026-10-17): career (unlocked levels), one level with the setting under test.
# Same steps as THPS1's dd-probe: a paused spot compared per factor (DD_AB), then a ride with frame times. Exploration only (optin).
# DD_RIGHTS: RIGHT presses at the level select; DD_TAG / DD_OUT: output; DD_ARGS: extra host args; DD_RIDE "lefty:frames ..." (x=... for leftx).
_DD_DIR = _os.path.join(_os.environ.get("DD_OUT", "/tmp/dd"), _os.environ.get("DD_TAG", "run"))
_DD_SHOT = lambda name: [("ctl", f"pcap 1 {_DD_DIR}/{name}"), ("wait", 3), ("ctl", "pcap 0"), ("wait", 10)]
# DD_AB "K[:S] ...": factor K, with `dd showall S` first when given (1:0 = the game's own picture inside `full`); DD_TRACE=1: `dltrace 1` after
# each shot (the frame's commands in the host log: which course items are drawn, tools in the private notes); DD_VTRACE=1 / DD_VRAMSAVE=1:
# the same, and a RAM dump, at the "vantage" frame (DD_WATCH runs).
_DD_TRACE = [("ctl", "dltrace 1"), ("wait", 5)] if _os.environ.get("DD_TRACE") else []
_DD_AB = [s for t in _os.environ.get("DD_AB", "1 2 4 8").split() for k, sa in [(t.split(":") + [""])[:2]] for s in (
    *([("ctl", f"dd showall {sa}")] if sa else []),
    ("ctl", f"dd factor {k}"), ("ctl", "dd reset"), ("wait", 20), *_DD_SHOT(f"start_x{k}{'_s' + sa if sa else ''}"), *_DD_TRACE, ("dl", 30, 0), ("ctl", "dd"))]
SESSIONS += [
    dict(name="dd-probe", config="dd-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro", "--hidden", "--unlock-levels", "--present-size", "960x540", "--aspect", "16:9", "--window", "1280x720",
               "--refresh", "60"] + _os.environ.get("DD_ARGS", "").split(),
         scenarios=[
        ("dd_probe", "draw distance: paused spot per factor (frame, triangles, buffers), camera swing, ride with frame times", [
            ("wait_for", "title"), ("go", "START", "title", "main_menu"),
            *CAREER_TO_GOALS[:-1],
            *[s for _ in range(int(_os.environ.get("DD_RIGHTS", "0"))) for s in (("press", "RIGHT"), ("wait", 45))],
            ("shot", "level_select"),
            ("press", "A"), ("wait", 150), ("shot", "goals"),
            # DD_WATCH=1: start counting at the run flag (gRunActive 0 -> 1), so DD_RIDE and the "vantage" frame land on the same game frame in
            # every run (THPS2/3 runs are repeatable from there; the load time before it is not).
            *([("ctl", "dd showall " + _os.environ["DD_SHOWALL"])] if _os.environ.get("DD_SHOWALL") else []),   # A/B of the zone visibility alone
            *([("press", "A"), ("ctl", "watch @gRunActive 1")] if _os.environ.get("DD_WATCH") else [("press", "A"), ("wait", 300)]),
            ("shot", "in_level"),
            ("ctl", "dd"),
            *([("ctl", f"ramsave {_DD_DIR}/ram_start.bin")] if _os.environ.get("DD_RAMSAVE") else []),
            # DD_PRE "KEY:frames ...": presses before the ride, with a shot after each (e.g. with --skip-to-restart in DD_ARGS: the pause menu's
            # SKIP TO RESTART to one of the course's restart points: repeatable spots all over the course)
            *[s for st in _os.environ.get("DD_PRE", "").split() for s in (("press", st.split(":")[0]), ("wait", int(st.split(":")[1])), ("shot", "pre"))],
            ("vpad", "attach"),
            *[s for st in _os.environ.get("DD_RIDE", "").split() for s in (
                (("ctl", f"vpad axis leftx {st.split(':')[0][2:]}"),) if st.startswith("x=") else (("ctl", f"vpad axis lefty {st.split(':')[0]}"),)) +
                (("wait", int(st.split(':')[1])),)],
            *(_DD_SHOT("vantage") if _os.environ.get("DD_WATCH") else []),
            *([("ctl", "dltrace 1"), ("wait", 2)] if _os.environ.get("DD_VTRACE") else []),
            *([("ctl", f"ramsave {_DD_DIR}/ram_vantage.bin")] if _os.environ.get("DD_VRAMSAVE") else []),
            ("ctl", "vpad axis lefty 0"), ("ctl", "vpad axis leftx 0"),
            *([("press", "START"), ("wait", 45)] if _os.environ.get("DD_PAUSE", "1") == "1" else []),
            *_DD_AB,
            # DD_CTL "cmd1;cmd2;..." at the paused spot after DD_AB (exploration: "dd factor 2;dltrace 1;dd factor 4;dltrace 1")
            *[s for c in _os.environ.get("DD_CTL", "").split(";") if c.strip() for s in (("ctl", c.strip()), ("wait", 20))],
            # DD_BUDGET "CAP [REST PASS MARGIN]": `dd dlbudget` at the paused spot (a shot of the same frame after it) and for the ride
            # (the byte budget forced to cut: near scenery and the game's own pass must stay)
            *([("ctl", "dd dlbudget " + _os.environ["DD_BUDGET"]), ("wait", 20), *_DD_SHOT("budget"), ("ctl", "dd")] if _os.environ.get("DD_BUDGET") else []),
            ("ctl", "dd mode " + _os.environ.get("DD_MODE", "original")),
            *([("ctl", "dd factor " + _os.environ["DD_FACTOR"])] if _os.environ.get("DD_FACTOR") else []),
            *([("ctl", "dd testcap " + _os.environ["DD_TESTCAP"])] if _os.environ.get("DD_TESTCAP") else []),
            ("ctl", "dd reset"),
            *([("press", "START"), ("wait", 45)] if _os.environ.get("DD_PAUSE", "1") == "1" else []),
            ("ctl", "vpad axis lefty 32767"), ("wait", 120), ("ctl", "vpad axis lefty 0"), ("wait", 40),
            *_DD_SHOT("back"),
            ("dl", 30, 0),
            ("ctl", "ftime start"),
            *([("ctl", f"pcap {_os.environ['DD_TOUR']} {_DD_DIR}/tour")] if _os.environ.get("DD_TOUR") else []),   # every Nth composited frame of the ride
            ("ctl", "vpad axis lefty -32767"),
            # DD_BURSTS=N: N short bursts of consecutive frames along the ride (b0, b1, ...: pairs of runs line up within a burst)
            *[s for k in range(int(_os.environ.get("DD_BURSTS") or "0")) for s in (("wait", 40), *_DD_SHOT(f"b{k}"),
                                                                              ("ctl", f"vpad axis leftx {(-32767, 0, 32767, 0)[k % 4]}"))],
            ("wait", 150),
            *_DD_SHOT("ride1"),
            *[s for k in range(6) for s in (("ctl", f"vpad axis leftx {32767 if k % 2 else -32767}"), ("wait", 20), ("ctl", "vpad axis leftx 0"), ("wait", 20))],
            *_DD_SHOT("ride2"),
            ("dl", 30, 0),
            *([("ctl", "pcap 0")] if _os.environ.get("DD_TOUR") else []),
            ("ctl", f"ftime stop {_DD_DIR}/ftime.csv"),
            ("ctl", "vpad axis lefty 0"), ("ctl", "vpad axis leftx 0"), ("wait", 20),
            ("ctl", "dd"), ("ctl", "stats"), ("ctl", "dd dlprobe"), ("ctl", "dd heap"),
        ]),
    ]),
]

# Draw distance in a two-player split screen (exploration, optin): the one-pad 2 PLAYER > TRICK ATTACK start of `two-players` (first course),
# then the same paused (THPS3: standing, DD_PAUSE=0) A/B as dd-probe (DD_AB, DD_TRACE, DD_ARGS, DD_OUT / DD_TAG) and a RAM dump.
SESSIONS += [
    dict(name="dd-2p", config="dd-2p-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro", "--hidden", "--present-size", "960x540", "--aspect", "16:9", "--window", "1280x720",
               "--refresh", "60"] + _os.environ.get("DD_ARGS", "").split(),
         scenarios=[
        ("dd_2p", "draw distance in a two-player split screen: paused spot per factor (frames, traces, buffers)", [
            *BOOT_TO_MENU,
            ("vpad", "attach"), ("vpress", "leftshoulder"),
            ("wait", 90),
            *[("vpress", "dpright"), ("wait", 40)] * 3,
            *[x for _ in range(10) for x in (("vpress", "a"), ("wait", 150))],
            ("wait_peek", "@gRunActive", 1, 60),
            ("wait", int(_os.environ.get("DD_SETTLE") or "60")),
            ("shot", "dd_2p_level"),
            *([("vpress", "start"), ("wait", 45)] if _os.environ.get("DD_PAUSE", "1") == "1" else []),
            ("ctl", f"ramsave {_DD_DIR}/ram_vantage.bin"),
            *_DD_AB,
            ("ctl", "dd showall auto"), ("ctl", "dd"), ("ctl", "dd heap"), ("ctl", "dd dlprobe"),
        ]),
    ]),
]

# Heap headroom with the always-allocated 2048-matrix pools (2026-10-22, the private development notes; optin, measurement): one career
# course (DH_COURSE: list position), loaded, skated ~12 s and ended from the pause menu (END RUN), `dd heap` (low-water marks since the
# start) after the load, after the ride and after the end. DD_ARGS: extra host args (e.g. "--draw-distance full", "--dd-buffers original").
_DH_PLAY = [("ctl", "vpad axis lefty -32767"),
            *[x for k in range(12) for x in (("ctl", f"vpad axis leftx {(-32767, 0, 32767, 0)[k % 4]}"),
                                             ("ctl", "vpad button a 1"), ("wait", 8), ("ctl", "vpad button a 0"), ("wait", 22))],
            ("ctl", "vpad axis lefty 0"), ("ctl", "vpad axis leftx 0")]
SESSIONS += [
    dict(name="dd-heap", config="dd-heap-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro", "--hidden", "--unlock-levels"] + _os.environ.get("DD_ARGS", "").split(), scenarios=[
        ("dd_heap", "heap headroom: one course, `dd heap` low-water marks", [
            ("wait_for", "title"), ("go", "START", "title", "main_menu"),
            *CAREER_TO_GOALS[:-1],
            *[s for _ in range(int(_os.environ.get("DH_COURSE", "0"))) for s in (("press", "RIGHT"), ("wait", 30))],
            ("shot", "select"),
            ("press", "A"), ("wait", 150), ("press", "A"), ("ctl", "watch @gRunActive 1"), ("wait", 30),
            ("shot", "in_level"), ("ctl", "dd heap"),
            ("vpad", "attach"), *_DH_PLAY,
            ("ctl", "dd heap"), ("ctl", "dd"),
            ("press", "START"), ("wait", 40), ("menu", "pause", 3), ("press", "A"), ("wait", 150), ("shot", "ended"),
            ("ctl", "dd heap"),
        ]),
    ]),
]

# Draw distance long run (2026-10-17): several courses back to back in one host, each played DD_LONG_S seconds with stick
# input, then pause -> END RUN and on through the end-of-run screens (DD_LONG_NAV: presses after END RUN) to the next course. Exploration
# only (optin): shots at every step, `dd` stats after each course (buffer peaks, governor), `stats` at the end.
_DDL_COURSES = [int(x) for x in _os.environ.get("DD_LONG_COURSES", "0 1 2").split()]   # increasing list positions
_DDL_PLAY = lambda s: [("ctl", "vpad axis lefty -32767"), *[x for k in range(max(1, s // 2)) for x in (
    ("ctl", f"vpad axis leftx {(-32767, 0, 32767, 0)[k % 4]}"), ("ctl", "vpad button a 1"), ("wait", 8), ("ctl", "vpad button a 0"), ("wait", 52))],
    ("ctl", "vpad axis lefty 0"), ("ctl", "vpad axis leftx 0")]
_DDL_NAV = [s for p in _os.environ.get("DD_LONG_NAV", "A:120 DOWN:20 DOWN:20 A:150").split() for s in (("press", p.split(":")[0]), ("wait", int(p.split(":")[1])), ("shot", "nav"))]
SESSIONS += [
    dict(name="dd-long", config="dd-long-config", fresh_pak=True, wav=False, optin=True,
         args=["--skip-intro", "--hidden", "--unlock-levels", "--present-size", "480x270", "--refresh", "60"] + _os.environ.get("DD_ARGS", "").split(),
         scenarios=[
        ("dd_long", "draw distance: several courses back to back (heap, buffers, governor)", [
            *([*BOOT_TO_MENU] if "BOOT_TO_MENU" in globals() and _os.environ.get("DD_LONG_BOOT3") else [("wait_for", "title"), ("go", "START", "title", "main_menu")]),
            *CAREER_TO_GOALS[:-1],
            *[s for i, c in enumerate(_DDL_COURSES) for s in (
                # the level select keeps its cursor on the last course: move by the difference
                *[x for _ in range(c - (_DDL_COURSES[i - 1] if i else 0)) for x in (("press", _os.environ.get("DD_LONG_KEY", "RIGHT")), ("wait", 30))],
                ("shot", f"select_{i}"),
                ("press", "A"), ("wait", 150), ("press", "A"), ("ctl", "watch @gRunActive 1"), ("vpad", "attach"),
                *([("wait", 30), ("ctl", f"ramsave {_DD_DIR}/long_a.bin"), ("wait", 300), ("ctl", f"ramsave {_DD_DIR}/long_b.bin")] if _os.environ.get("DD_LONG_RAMSAVE") and i == 0 else []),
                *([] if _os.environ.get("DD_LONG_NODD") else [("ctl", "dd reset")]), ("ctl", "ftime start"),   # DD_LONG_NODD: a host without `dd` (v0.1)
                *_DDL_PLAY(int(_os.environ.get("DD_LONG_S", "120"))),
                ("ctl", "ftime stop"), *([] if _os.environ.get("DD_LONG_NODD") else [("ctl", "dd"), ("ctl", "dd heap")]), ("shot", f"played_{i}"),
                # DD_LONG_TIMEOUT=1: the run ends by itself (career 2:00; DD_LONG_S >= 125), not from the pause menu (the course-cycle crash, 2026-10-17)
                *([("wait", 40), ("shot", f"timeup_{i}")] if _os.environ.get("DD_LONG_TIMEOUT") else
                  [("press", "START"), ("wait", 40), ("menu", "pause", 3), ("press", "A"), ("wait", 120), ("shot", f"endrun_{i}")]),
                *_DDL_NAV,
            )],
            ("ctl", "stats"), *([] if _os.environ.get("DD_LONG_NODD") else [("ctl", "dd heap")]),
        ]),
    ]),
]
# Course cycle (src/music.cpp; the crash after a few courses, 2026-10-17): The Hangar, School II, NY City, Venice Beach back to back
# (Marseille, a competition, ends with a different menu), each ended from the pause menu. The level select keeps its cursor on the last
# course; END RUN -> statistics -> A -> the run-over menu -> LEVEL SELECT (third entry).
from course_cycle import course_cycle_session  # noqa: E402
SESSIONS += [course_cycle_session(
    "course-cycle", [*BOOT_TO_MENU, *CAREER_TO_GOALS[:-1]],
    [[], [("press", "RIGHT"), ("wait", 30)], [("press", "RIGHT"), ("wait", 30), ("press", "RIGHT"), ("wait", 30)], [("press", "RIGHT"), ("wait", 30)]],
    [("press", "A"), ("wait", 150), ("press", "A"), ("wait_peek", "@gRunActive", 1, 60)],
    [("press", "START"), ("wait", 40), ("menu", "pause", 3), ("press", "A"), ("wait", 120), ("press", "A"), ("wait", 20),
     ("press", "DOWN"), ("wait", 20), ("press", "DOWN"), ("wait", 20), ("press", "A"), ("wait", 150)],
)]

# Two players in widescreen (v0.2, rt64-splitscreen-widescreen.patch + hud_anchor.cpp): the side-by-side split screen fills the wide picture,
# each view widened like the one-player camera (`split` views > 0), each player's HUD block at its own view's edge (the game mirrors player 2's
# HUD to the right of its view: groups at q0 and q4), both pads on their own ports. present_split: in each side band outside the central 4:3
# area >= 90 % of the columns are drawn. Then `split off` (live) for a before picture. `169-hudorig`: HUD Placement `original` places the
# split screen's HUD the same way (the views fill the picture; the 4:3 spot would leave each HUD inside its view), so the same groups are expected.
SESSIONS += [
    dict(name=f"two-players-{var}", config=f"two-players-{var}-config", fresh_pak=True, wav=False, present_every=10,
         args=["--skip-intro", "--hidden", "--aspect", asp, "--window", win, "--res-scale", "2", *extra], scenarios=[
        (f"two_players_{var}", f"two players at {asp}{' (hud original)' if extra else ''}: the split screen fills the picture, each HUD at its view's edge, each pad on its port", [
            *_TWO_PADS_TO_LEVEL,
            ("wait", 60),
            ("present_split", win, 0.90),
            ("keep_present", f"two_players_{var}_after"),
            ("ctl_match", "split", r"wide=1 views=[1-9]\d* .* hud_tasks=[1-9]\d* groups q0=[1-9]\d* .* q4=[1-9]\d* "),
            ("ctl_match", "hud", r"mode=%s " % ("original" if extra else "expand")),
            *_TWO_PADS_PORTS,
            ("ctl", "split off"), ("wait", 20), ("keep_present", f"two_players_{var}_before"),
        ]),
    ])
    for (var, asp, win, extra) in (("169", "16:9", "1280x720", []), ("219", "21:9", "1680x720", []),
                                   ("169-hudorig", "16:9", "1280x720", ["--hud", "original"]))
]

# Two players with split original (hud expand): each player's HUD stays with its view in the 4:3 middle (hud_sessions.two_players_split_original).
from hud_sessions import two_players_split_original  # noqa: E402
SESSIONS.append(two_players_split_original(_TWO_PADS_TO_LEVEL))
# Border crop (graphics setting `border`, src/border_crop.cpp): the shared tests/crop_sessions.py.
from crop_sessions import crop_sessions  # noqa: E402
SESSIONS += crop_sessions([*CAREER_TO_GOALS, ("go", "A", "goals", "in_level", 90)], boot=BOOT_TO_MENU, pause=[("go", "START", "in_level", "pause")])
# Border crop in a two-player split screen at 16:9: each view's own inset scissor goes to the frame's edges too (crop_sessions.crop_two_players).
from crop_sessions import crop_two_players  # noqa: E402
SESSIONS.append(crop_two_players(_TWO_PADS_TO_LEVEL, [("ctl", "vpad button start 1"), ("wait", 10), ("ctl", "vpad button start 0"), ("wait", 45)]))
# Level-start freeze (v0.2 queue item 3, tests/load_freeze.py): the course cycle's four starts with frame timestamps over each load
# phase (A on the level select, A on the goals). `lf-probe` (optin) runs in a visible window; THPS_LF_SAMPLE=8 adds a `sample`.
from load_freeze import load_freeze_session  # noqa: E402
_LF = dict(
    to_select=[*BOOT_TO_MENU, *CAREER_TO_GOALS[:-1]],
    courses=[[], [("press", "RIGHT"), ("wait", 30)], [("press", "RIGHT"), ("wait", 30), ("press", "RIGHT"), ("wait", 30)], [("press", "RIGHT"), ("wait", 30)]],
    phases=[("A", []), ("A", [("wait_peek", "@gRunActive", 1, 60)])],
    end_run=[("press", "START"), ("wait", 40), ("menu", "pause", 3), ("press", "A"), ("wait", 120), ("press", "A"), ("wait", 20),
             ("press", "DOWN"), ("wait", 20), ("press", "DOWN"), ("wait", 20), ("press", "A"), ("wait", 150)],
)
SESSIONS += [load_freeze_session("lf-probe", **_LF, hidden=False, optin=True, limits={"composited": 1000.0, "game": 1000.0})]
# The suite's check (hidden window, the first three courses): the median over the three starts of the longest gap between game
# frames while the course loads stays under LF_GAME_MS (one preempted window on a busy machine does not fail it; a warning only
# when the machine is overloaded). Before the v0.2 fixes (ERZ decoder, native memset / memcpy) every start was over it.
LF_GAME_MS = 140.0   # 2026-10-18: 104-120 ms after the fixes, 134-174 ms before (load 4-6)
SESSIONS += [load_freeze_session("lf-check", **{**_LF, "courses": _LF["courses"][:3]}, limits={"game": 1000.0}, median=("game", LF_GAME_MS))]

# Draw distance's matrix pools (2026-10-22, the private development notes): with dd_buffers = bigger (the default) the game gets pools of
# 2048 matrices at every course start and keeps its own cap (420) at `original`, so the setting takes effect at once, both ways; with
# --dd-buffers original the game's own pools (420) whatever the setting.
_DDB_TO_LEVEL = [("wait_for", "title"), ("go", "START", "title", "main_menu"), *CAREER_TO_GOALS[:-1], ("press", "A"), ("wait", 150), ("press", "A"), ("ctl", "watch @gRunActive 1"), ("wait", 30)]
SESSIONS += [
    dict(name="dd-buffers", config="dd-buffers-config", fresh_pak=True, wav=False,
         args=["--skip-intro", "--hidden", "--draw-distance", "original", "--dd-buffers", "bigger"], scenarios=[
        ("dd_buffers_now", "default buffers: pools of 2048 with the game's cap 420 at Original; Full raises the cap at once, Original puts it back", [
            *_DDB_TO_LEVEL,
            ("ctl_match", "dd heap", r"mtx_pool 2048 mtx_cap 420 "),
            ("ctl_match", "dd", r"buffers=bigger .* mtx_cap=420 "),
            ("ctl", "dd mode full"), ("wait", 30),
            ("ctl_match", "dd heap", r"mtx_pool 2048 mtx_cap 2048 "),
            ("ctl_match", "dd", r"mtx_cap=2048 "),
            ("ctl", "dd mode original"), ("wait", 30),
            ("ctl_match", "dd heap", r"mtx_pool 2048 mtx_cap 420 .* failed_calls 0 "),
        ]),
    ]),
    dict(name="dd-buffers-own", config="dd-buffers-own-config", fresh_pak=True, wav=False,
         args=["--skip-intro", "--hidden", "--draw-distance", "original", "--dd-buffers", "original"], scenarios=[
        ("dd_buffers_own", "--dd-buffers original: the game's own pools (420), at Original and at Full", [
            *_DDB_TO_LEVEL,
            ("ctl_match", "dd heap", r"mtx_pool 420 mtx_cap 420 "),
            ("ctl_match", "dd", r"buffers=original .* mtx_cap=420 "),
            ("ctl", "dd mode full"), ("wait", 30),
            ("ctl_match", "dd heap", r"mtx_pool 420 mtx_cap 420 "),
            ("ctl", "dd mode original"),
        ]),
    ]),
    # Opt-in demo: NY City at Original, then Graphics > Draw Distance > Full in the menu in the middle of the run, a ride: the pool use goes past
    # the game's 420 with no restart (`dd`: mtx_hw > 420, mtx_capped=0). DD_ARGS: extra host args.
    dict(name="dd-switch", config="dd-switch-config", fresh_pak=True, wav=False, optin=True, requires="menu",
         fresh_files=["graphics.cfg"],
         args=["--skip-intro", "--hidden", "--unlock-levels", "--window", "1280x720", "--draw-distance", "original"] + _os.environ.get("DD_ARGS", "").split(), scenarios=[
        ("dd_switch", "switch Original -> Full in the menu mid-run: the matrix pool use passes 420 at once", [
            ("wait_for", "title"), ("go", "START", "title", "main_menu"), *CAREER_TO_GOALS[:-1],
            *[s for _ in range(3) for s in (("press", "RIGHT"), ("wait", 30))],
            ("shot", "select"),
            ("press", "A"), ("wait", 150), ("press", "A"), ("ctl", "watch @gRunActive 1"), ("wait", 30),
            ("shot", "in_level_original"),
            ("ctl", "dd reset"), ("wait", 60),
            ("ctl_match", "dd", r"mode=original .* mtx_cap=420 "),
            ("ui", "esc"), ("ui_state", "open=1"), ("ui", "tab 2"), ("ui", "click #lbl_dd_full"), ("log", r"draw distance: full"), ("ui", "esc"),
            ("ctl", "dd reset"),
            ("vpad", "attach"),
            ("ctl", "vpad axis lefty -32767"), ("wait", 150),
            *[s for k in range(6) for s in (("ctl", f"vpad axis leftx {32767 if k % 2 else -32767}"), ("wait", 20), ("ctl", "vpad axis leftx 0"), ("wait", 20))],
            ("ctl", "vpad axis lefty 0"), ("wait", 30),
            # pause -> RETRY: the run starts again (the game is not restarted); the course's start view is the busy one
            ("press", "START"), ("wait", 40), ("press", "DOWN"), ("wait", 10), ("press", "A"), ("wait", 200),
            ("shot", "in_level_full"),
            ("ctl_match", "dd", r"mode=full .* mtx_hw=(42[1-9]|4[3-9]\d|[5-9]\d\d|1\d\d\d|20[0-4]\d) mtx_cap=2048 "),   # past the game's 420, no restart
            ("ctl_match", "dd", r"mtx_capped=0 "),
            ("ctl", "dd heap"),
        ]),
    ]),
]

# Draw distance stress (2026-10-23, the bigger display lists, the governor's ramp and the byte budget; optin): Full from the start. School
# II (the course that overran its 72 KiB display list) started DD_STRESS_N times (pause > RETRY runs the course gfx set-up again): each
# time the first ride with camera turns and quick setting changes (Original, Full, 2x, Full, a few frames apart); then END RUN and the
# same rides in NY City and Philadelphia. The session sets THPS_DD_CANARY=1 (guard bytes after the display lists) and checks that the
# guards are on (`dd dlprobe` canary 1; until 2026-10-26 it only asked for the variable in this comment, and `canary_bad 0` passed with no
# guard at all). Expected: no guard word changed, no budget cut at the default budget, no panic, no failed heap request. The forced cuts
# are dd-cut's.
_DS_RIDE = [("ctl", "vpad axis lefty -32767"),
            *[x for k in range(6) for x in (("ctl", f"vpad axis leftx {(-32767, 32767)[k % 2]}"), ("wait", 15), ("ctl", "vpad axis leftx 0"), ("wait", 10))],
            ("ctl", "dd mode original"), ("wait", 4), ("ctl", "dd mode full"), ("wait", 4), ("ctl", "dd mode 2x"), ("wait", 4), ("ctl", "dd mode full"),
            *[x for k in range(4) for x in (("ctl", f"vpad axis leftx {(32767, -32767)[k % 2]}"), ("wait", 20))],
            ("ctl", "vpad axis lefty 0"), ("ctl", "vpad axis leftx 0"), ("wait", 45)]
_DS_END = [("press", "START"), ("wait", 40), ("menu", "pause", 3), ("press", "A"), ("wait", 120), ("press", "A"), ("wait", 20),
           ("press", "DOWN"), ("wait", 20), ("press", "DOWN"), ("wait", 20), ("press", "A"), ("wait", 150)]
_DS_START = [("press", "A"), ("wait", 150), ("press", "A"), ("wait_peek", "@gRunActive", 1, 60), ("vpad", "attach")]
_DS_CHECK = [("ctl_match", "dd", r"mode=full .* backoffs=\d+ panics=0 cuts=0 "), ("ctl_match", "dd dlprobe", r"canary 1 frames \d+ canary_bad 0 "),
             ("ctl_match", "dd heap", r" dl 147456 .* dl_fallbacks 0 .* failed_calls 0 ")]
SESSIONS += [
    dict(name="dd-stress", config="dd-stress-config", fresh_pak=True, wav=False, optin=True, env={"THPS_DD_CANARY": "1"},
         args=["--skip-intro", "--hidden", "--unlock-levels", "--draw-distance", "full", "--dd-buffers", "bigger"] + _os.environ.get("DD_ARGS", "").split(), scenarios=[
        ("dd_stress", "School II starts and first rides, setting changes, camera turns; NY City and Philadelphia: guard bytes intact, no cut", [
            ("wait_for", "title"), ("go", "START", "title", "main_menu"), *CAREER_TO_GOALS[:-1],
            ("press", "RIGHT"), ("wait", 30), ("shot", "select_school2"),
            *_DS_START, ("ctl", "dd reset"),
            *[x for _ in range(int(_os.environ.get("DD_STRESS_N", "4"))) for x in (
                *_DS_RIDE, ("shot", "school2_ride"),
                ("press", "START"), ("wait", 40), ("menu", "pause", 1), ("press", "A"), ("wait", 150), ("vpad", "attach"))],
            *_DS_RIDE, ("ctl", "dd"), *_DS_CHECK, *_DS_END,
            ("press", "RIGHT"), ("wait", 30), ("press", "RIGHT"), ("wait", 30), ("shot", "select_ny"),
            *_DS_START, *_DS_RIDE, ("shot", "ny_ride"), ("ctl", "dd"), *_DS_CHECK, *_DS_END,
            *[x for _ in range(3) for x in (("press", "RIGHT"), ("wait", 30))], ("shot", "select_philly"),
            *_DS_START, *_DS_RIDE, ("shot", "philly_ride"), ("ctl", "dd"), *_DS_CHECK,
        ]),
    ]),
]
# A RETRY and the zone record (review 2026-10-26, finding 7): School II at Full. RETRY runs the course set-up again and rebuilds the item
# list at the same address and count, so the record (which items the zone culling hid, which an event owns) must start again: an item made
# event-owned in the first run (`dd own`, as an event naming it would) is not after the RETRY, and the items the set-up named are the same
# number as before. Then the governor across a transition (finding 6, deterministic): `dd stale 99` gives a 99 % sample measured across a
# transition and one built before it, in one critical section: both dropped, Full keeps its ceiling; `dd feed 99` (the control case) gives
# a current one once the settle is over: it panics.
_DR_ITEM = 7
SESSIONS += [
    dict(name="dd-retry", config="dd-retry-config", fresh_pak=True, wav=False,
         args=["--skip-intro", "--hidden", "--unlock-levels", "--draw-distance", "full", "--window", "960x540"], scenarios=[
        ("dd_retry_zone", "an item an event owned in the last run is the game's again after RETRY; the set-up's own names are kept", [
            *_fs_to_run(1, 30),
            ("ctl_match", f"dd item {_DR_ITEM}", r" event 0 "),
            ("ctl_same", f"dd item {_DR_ITEM}", r" named (\d+) ", "named"),
            ("ctl_match", f"dd own {_DR_ITEM}", r" event 1 "),
            ("press", "START"), ("wait", 40), ("menu", "pause", 1), ("press", "A"), ("wait", 150), ("wait_peek", "@gRunActive", 1, 60), ("wait", 30),
            ("ctl_match", f"dd item {_DR_ITEM}", r" event 0 "),
            ("ctl_same", f"dd item {_DR_ITEM}", r" named (\d+) ", "named"),
            ("ctl_match", "dd", r"course_starts=[2-9]"),
        ]),
        ("dd_stale_feedback", "a stale buffer sample after a setting change is dropped; a current one still acts", [
            ("ctl", "dd mode full"), ("wait", 10), ("ctl", "dd reset"),
            ("ctl_match", "dd stale 99", r"ceiling=64\.00 .* panics=0 .* stale_dropped=1 settle_dropped=[1-9]"),
            ("wait", 10),
            ("ctl_match", "dd feed 99", r"ceiling=(?!64\.00)\d.* panics=1 "),
            ("ctl_match", "dd mode full", r"ceiling=64\.00 "),
        ]),
    ]),
]
# The display-list budget with a forced cap (review 2026-10-26, findings 9 and 10): School II at Full with `dd dlbudget CAP` (DD_CUT_CAP,
# bytes) so tight that only some of the extra passes fit. The nearest extra items are reserved before the first pass with every pass at
# its bound, so the cuts leave out the farthest and none is made after the passes began (late_cuts=0: before the fix the passes after the
# first were counted at their average and an expensive far pass left the nearest ones out). The guard bytes are on (THPS_DD_CANARY) and
# intact. dd-stress checks the default budget (no cut at all).
_DC_RIDE = [("ctl", "vpad axis lefty -32767"),
            *[x for k in range(8) for x in (("ctl", f"vpad axis leftx {(-32767, 32767)[k % 2]}"), ("wait", 15), ("ctl", "vpad axis leftx 0"), ("wait", 10))],
            ("ctl", "vpad axis lefty 0"), ("wait", 20)]
SESSIONS += [
    dict(name="dd-cut", config="dd-cut-config", fresh_pak=True, wav=False, env={"THPS_DD_CANARY": "1"},
         args=["--skip-intro", "--hidden", "--unlock-levels", "--draw-distance", "full", "--window", "960x540"], scenarios=[
        ("dd_cut", "a forced display-list budget: the farthest extra items are left out before the passes, never the nearest after them", [
            *_fs_to_run(1, 30), ("vpad", "attach"),
            ("ctl_match", "dd dlprobe", r"canary 1 "),
            ("ctl", f"dd dlbudget {_os.environ.get('DD_CUT_CAP', '81920')} 0 0 0"), ("ctl", "dd reset"),
            *_DC_RIDE,
            ("ctl_match", "dd", r"cuts=[1-9]\d* cut_items=[1-9]\d* late_cuts=0 "),
            ("ctl_match", "dd dlprobe", r"canary 1 frames \d+ canary_bad 0 "),
            ("ctl", "dd dlbudget 0 0 0 0"),
        ]),
    ]),
]
# The bigger buffers on a constrained heap (review 2026-10-26, finding 1): THPS_DD_HEAP_FREE makes the planning see a free list of the given
# blocks from the course set-up's start, and every set-up request is taken from that view (`dd heap` view_fail counts the ones it could
# not have satisfied: the real allocator hangs there). One block of 266,240 bytes holds the game's own set-up (2 x 72 KiB lists, the
# matrix and vertex pools: 217,392) but not one 144 KiB list more: everything stays the game's size and nothing fails (before the fix the
# first list was enlarged and the second one's native size no longer fitted). With 600,000 + 900,000 bytes the lists and the matrix pools
# fit the first block and are enlarged (the second block, the one later requests rely on, is not touched).
_DHP_TO_COURSE = [*_fs_to_run(0, 30)]
SESSIONS += [
    dict(name="dd-heap-plan", config="dd-heap-plan-config", fresh_pak=True, wav=False, env={"THPS_DD_HEAP_FREE": "266240"},
         args=["--skip-intro", "--hidden", "--draw-distance", "full", "--window", "960x540"], scenarios=[
        ("dd_heap_plan_tight", "a free list with room for the game's own set-up only: every buffer the game's size, no request that would fail", [
            *_DHP_TO_COURSE,
            ("log", r"draw distance: WARNING no room for a 147456-byte display list \(request 1"),
            ("ctl_match", "dd heap", r"mtx_pool 420 .* dl 73728 dl_game 73728 .* failed_calls 0 .* view_fail 0"),
        ]),
    ]),
    dict(name="dd-heap-plan-room", config="dd-heap-plan-config", fresh_pak=True, wav=False, env={"THPS_DD_HEAP_FREE": "600000,900000"},
         args=["--skip-intro", "--hidden", "--draw-distance", "full", "--window", "960x540"], scenarios=[
        ("dd_heap_plan_room", "room for the bigger lists and matrix pools in the first block: both enlarged, nothing fails", [
            *_DHP_TO_COURSE,
            ("ctl_match", "dd heap", r"mtx_pool 2048 .* dl 147456 dl_game 73728 .* failed_calls 0 .* view_fail 0"),
        ]),
    ]),
]
