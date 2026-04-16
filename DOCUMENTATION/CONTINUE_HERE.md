# Cube Jump — Continue Here

Use this file when you open the project from USB (or later) to see everything that’s done and where to pick up.

---

## What this is

**Cube Jump** is a 2D PC game made in **Python + pygame**. You control a cube with a face through a scrolling pipe: glide with the mouse (or flap with any key), pass through gaps without hitting the walls. Goals: **Normal** = 999 gaps for a secret surprise; **Time attack** = 30 gaps in 60 seconds.

---

## Quick start (on a new machine)

1. **Python 3.8+** installed.
2. In the game folder:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```
3. Optional: put your own **music.mp3** in the same folder as `main.py` for background music.

---

## Project layout

| Path | Purpose |
|------|--------|
| **main.py** | Full game (all features). **This is the only file you need to run the game.** |
| **requirements.txt** | `pygame>=2.5.0` |
| **README.md** | Player-facing: how to play, controls, setup. |
| **CONTINUE_HERE.md** | This file — project state and handoff. |
| **DEVLOG.md** | Structured devlog (v1–v8). |
| **VERSIONS_README.md** | Human-style “what we did + fake problems” per version. |
| **versions/** | Old snapshots: v01_initialise_pygame.py … v08_final.py (for reference, not needed to run). |
| **music.mp3** | Your background track (optional; game runs without it). |

---

## Everything that’s implemented

### Core gameplay
- **Pipe:** Segments with random gaps scroll left. Cube must pass through gaps; hitting top/bottom wall = game over.
- **Controls:** **Mouse** = cube follows cursor (vertical). **Flap** = gravity + jump on any key except ESC/TAB (Flappy Bird style). Toggle in mod menu (TAB → C).
- **Scoring:** +1 per gap passed. **Normal** goal = 999 (then “secret surprise” screen). **Time attack** goal = 30 gaps in 60 seconds.
- **Difficulty:** Easy / Medium / Hard (start screen: 1 / 2 / 3). Affects scroll speed, pipe spacing, gap size. Params in `DIFFICULTIES` in main.py.
- **Physics:** All movement uses **delta time** (per-second speeds) so behaviour is the same at any FPS.
- **Hitbox:** Collision uses a **rounded rectangle** (border_radius 6) matching the drawn cube, not a full 44×44 box.

### Modes and screens
- **Start screen:** Title, “Glide through the pipe…”, difficulty (1/2/3), mode (4=Normal, 5=Time attack), theme (G). SPACE or click to play. Title pulses to music (or time if no music).
- **Time attack:** 60s countdown in HUD; win at 30 gaps, lose on time-out or pipe hit. Win screen shows time taken.
- **Game over / Win:** Overlay + “SPACE to retry”. Retry keeps same difficulty and mode.

### Mod menu (TAB during play)
- Pauses the game.
- **H** – Show hitbox (green rounded outline).
- **C** – Control: Mouse / Flap.
- **G** – Theme: Classic / Neon / Minimal.
- **F** – Fullscreen on/off.
- **R** – Ghost replay on/off (replay last run as semi-transparent cube).
- **Q / A** – Music volume up/down.
- **Z / X** – SFX volume up/down (for future sounds).
- **TAB** again to close and resume.

### Themes (visual skins)
- **Classic:** Dark bg, blue cube, grey pipes.
- **Neon:** Dark purple bg, cyan cube, purple pipes.
- **Minimal:** Light grey bg, dark grey cube and pipes.  
Colors live in `THEMES` at top of main.py; used for background, pipes, cube, HUD.

### Other features
- **Fullscreen:** F11 anytime, or Mod menu → F. Exiting fullscreen returns to 1920×1080.
- **Cursor:** **T** to hide/show mouse cursor (position still works when hidden).
- **Music:** Loads `music.mp3` from the game folder if present; volume from mod menu (Q/A). `MUSIC_FILENAME` and `load_music(volume)` in main.py.
- **Ghost replay:** After each run, path is saved. With “Ghost replay” ON in mod menu, next run shows last run as a semi-transparent ghost synced by elapsed time (race yourself).

---

## Where things are in main.py (approx. line ranges)

- **Top ~60 lines:** Constants (`WINDOW_W`, `WINDOW_H`, `DIFFICULTIES`, `THEMES`, `TIME_ATTACK_*`, `HOME_BEAT_*`, etc.).
- **~61–70:** `get_asset_path`, `load_music`.
- **~71–95:** Collision helpers (`_circle_rect_overlap`, `rounded_rect_collides_rect`).
- **~96–165:** `PipeSegment` class, `spawn_segment`, `draw_cube_with_face` (takes theme dict and optional `ghost_alpha`).
- **~166–570:** `run_game()`: init, state vars, main loop (events, start screen, game update, drawing, mod menu, game over, win). Uses `win_w`/`win_h` so fullscreen works.

State to keep in mind when editing: `on_play_screen`, `game_mode` ("normal" / "time_attack"), `difficulty`, `theme`, `mod_menu_open`, `show_hitbox`, `control_mode`, `show_ghost`, `ghost_data`, `current_run_recording`, `elapsed_time`, `time_attack_remaining`, `fullscreen`, `music_volume`, `sfx_volume`.

---

## Tuning (constants in main.py)

- **Window:** `WINDOW_W`, `WINDOW_H` (default 1920×1080).
- **Difficulty:** `DIFFICULTIES` — `base_scroll`, `speed_per_point`, `pipe_gap_min/max`, `gap_h_min/max` for easy/medium/hard.
- **Time attack:** `TIME_ATTACK_GOAL` (30), `TIME_ATTACK_SECONDS` (60.0).
- **Normal goal:** `GOAL_SCORE` (999).
- **Music:** `MUSIC_FILENAME` ("music.mp3"). Home screen pulse: `HOME_BEAT_INTERVAL_MS`, `HOME_BEAT_PULSE_SCALE`, `HOME_BEAT_DECAY`.
- **Flap:** `GRAVITY`, `FLAP_IMPULSE`, `MAX_FALL_SPEED`.
- **Cube:** `CUBE_SIZE`, `CUBE_BORDER_RADIUS`, `CUBE_SMOOTH_SPEED`.
- **Themes:** `THEMES` dict (add or change keys/colors there).

---

## Ideas discussed but not implemented (yet)

- **Sound effects:** Pass gap, game over, menu click — use `sfx_volume` when you add them.
- **Pre-analyzed music:** Beat/amplitude from MP3 for better home-screen or in-game reaction (e.g. aubio/librosa, save data, drive visuals from `get_pos()`).
- **High scores:** Save best score (and per-difficulty) to a file, show on HUD or game over.
- **Power-ups:** Shield, slow-mo, double points, etc.
- **Particles / juice:** Burst on gap pass, trail, screen shake on death.
- **More themes or cube expressions:** E.g. face changes when close to wall or when scoring.

---

## Version snapshots (versions/)

- **v01** – Pygame init, window, quit.
- **v02** – Static cube.
- **v03** – Mouse control.
- **v04** – Pipe scrolling.
- **v05** – Collision, scoring, game over.
- **v06** – HUD, difficulty cap, 999 goal, surprise screen.
- **v07** – Delta-time (FPS-independent).
- **v08** – Cube face, music.

The current **main.py** has everything above plus: play screen, difficulty (easy/medium/hard), mod menu, hitbox toggle, flap mode, rounded hitbox, time attack, themes, ghost replay, fullscreen, volume, cursor toggle. The version files are for reference only; they do not include these later features.

---

## Checklist when moving to a new PC / USB

- [ ] Python 3.8+ installed  
- [ ] `pip install -r requirements.txt` in the game folder  
- [ ] Copy **music.mp3** into the folder if you want music  
- [ ] Run: `python main.py`  
- [ ] Open **CONTINUE_HERE.md** (this file) to see what’s done and where to continue  

You can continue by editing **main.py** and/or adding new files (e.g. sounds, high-score file); all core logic and features are in **main.py**.
