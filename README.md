# Cube Jump

A 2D game made in Python with pygame for PC. Control a cube with a face through a scrolling pipe using your mouse.

**Continuing the project later (e.g. from USB)?** See [CONTINUE_HERE.md](CONTINUE_HERE.md) for what’s implemented and where to pick up.

For a step-by-step development story and runnable versions from “blank window” to full game, see [VERSIONS_README.md](VERSIONS_README.md) (version-by-version + fake dev problems), [DEVLOG.md](DEVLOG.md), and the `versions/` folder (e.g. `python versions/v01_initialise_pygame.py` through `v08_final.py`).

## How to play

- **Control:** Move your mouse up and down to glide the cube through the pipe (or switch to **Flap** mode in the mod menu and use any key to jump, Flappy Bird style).
- **Goal:** Reach **30 gaps**. In **Time attack**, do it within **60 seconds**.
- **Rules:** Slide smoothly into each gap; hitting the wall ends the run. In time attack, running out of time also ends the run.
- **Difficulty:** Scroll speed increases as you score (capped after 50 gaps). Choose **Easy**, **Medium**, or **Hard** on the start screen (see below).

## Time attack (start screen)

Press **5** on the start screen to select **Time attack** mode. You have **60 seconds** to pass through **30 gaps**. A countdown timer appears in the HUD. Win by reaching 30 gaps before time runs out. Press **4** for Normal mode, or **6** for Flappy mode.

## Theme / skin (start screen or mod menu)

Choose a visual theme:

- **Classic:** Dark background, blue cube, grey pipes.
- **Neon:** Dark purple background, cyan cube, purple pipes.
- **Minimal:** Light grey background, dark grey cube and pipes.

On the start screen press **G** to cycle theme. In the mod menu (TAB), press **G** to change theme.

## Ghost replay (mod menu)

After a run ends (game over or win), that run is saved. In the mod menu (TAB), turn **Ghost replay** ON (**R**). On your next run, a semi-transparent “ghost” cube replays your last run so you can race yourself. The ghost follows the same timeline (by elapsed time), so you can see how you’re doing compared to the previous attempt.

## Fullscreen and volume

- **Fullscreen:** Press **F11** anytime to toggle fullscreen. Or open the mod menu (TAB) and press **F**.
- **Volume:** In the mod menu (TAB), **Q** / **A** adjust music volume, **Z** / **X** adjust SFX volume (for future sound effects). Percentages are shown in the menu.
- **Game speed slider:** In the mod menu, use **LEFT/RIGHT** to change game speed from **50% to 150%**.
- **Audio speed/pitch sync:** Enabled only when supported by your installed `pygame` build. If unsupported, music stays at normal playback speed.

## Difficulty (start screen)

On the start screen, pick a difficulty before you play:

- **Easy** (press **1**): Slower scroll, more space between pipes, larger gaps. Best for learning the game.
- **Medium** (press **2**): Default balance of speed and gap size.
- **Hard** (press **3**): Faster scroll, pipes closer together, smaller gaps.

Your choice is shown under the title; press **SPACE** or click to start.

## Mod menu (TAB)

Press **TAB** during gameplay to open the mod menu. The game pauses while the menu is open. Press **TAB** again to close and resume.

- **Show hitbox (H):** Toggle ON to see the cube’s real collision box (green outline). The hitbox is centered and about **30% smaller** than the visual cube.
- **Control (C):** Switch between **Mouse** and **Flap** (any key to jump).
- **Theme (G):** Cycle Classic / Neon / Minimal.
- **Fullscreen (F):** Toggle fullscreen.
- **Ghost replay (R):** Show last run as a semi-transparent ghost cube.
- **Music (Q/A):** Increase / decrease music volume.
- **SFX (Z/X):** Increase / decrease SFX volume (for future sounds).
- **Game speed (LEFT/RIGHT):** Slow down or speed up gameplay (50%-150%).

## Setup

1. Install Python 3.8+ and create a virtual environment (optional).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. To play your own background music, put your MP3 file in this folder and either:
   - Name it `music.mp3`, or
   - Open `main.py` and set `MUSIC_FILENAME = "yourfile.mp3"` at the top.

## Run

```
python main.py
```

- **ESC** or window close: quit  
- **1 / 2 / 3** on start screen: difficulty (Easy / Medium / Hard)  
- **4 / 5 / 6** on start screen: Normal / Time attack / Flappy mode  
- **G** on start screen: cycle theme (Classic / Neon / Minimal)  
- **SPACE** (or **Enter**) or click on start screen: play  
- **SPACE** after game over or win: play again  
- **TAB:** open/close mod menu  
- **F11** or **F** (in mod menu): fullscreen  
- **T:** hide/show cursor  
- **LEFT / RIGHT** (in mod menu): game speed slider  
- **Flap mode:** any key except ESC or TAB to jump  

## Technical notes

- All movement and scrolling use **delta time** (per-second speeds), so gameplay is the same at any frame rate (e.g. 30, 60, 120+ FPS).
- Gameplay speed can be adjusted live in the mod menu (50%-150%).
- Player collision uses a centered hitbox that is ~30% smaller than the drawn cube (visual size is unchanged).
- The HUD at the top shows how many gaps you’ve passed and the active mode goal.
- Reaching the goal triggers the win/surprise screen.

---

## Coursework Evidence (Unit 2B)

This section is written to match your evidence checklist and deadline items.

### 📋 User Requirements & Purpose of the Software (2B.P2)

#### User requirements (ages 7+)

- Target users are children aged 7+, beginner players, and casual players.
- Players need very simple controls, clear goals, immediate feedback, and short game sessions.
- The game must:
  - Run on school/home PCs with keyboard and mouse.
  - Be easy to start (`SPACE` or click).
  - Avoid inappropriate content.
  - Provide adjustable difficulty (`Easy`, `Medium`, `Hard`).
  - Include clear failure/win conditions.

#### Intended purpose of software

- **Primary purpose:** entertainment through quick arcade-style challenge.
- **Secondary value (educational):**
  - Hand-eye coordination and reaction timing.
  - Pattern recognition (gap spacing and rhythm).
  - Basic strategy (choosing difficulty and mode).
  - Perseverance through retry loops.

#### Project name choice

- **Project name:** `Cube Jump`
- **Reason:** the player controls a cube and repeatedly jumps/glides through pipe gaps. The name is short, age-appropriate, and easy to remember.

### ⚠️ Problem Definition Statement (2B.P3)

#### Technical issues anticipated + required functionality

- Keep movement smooth across different FPS values (solved with delta-time updates).
- Handle collision accurately with rounded cube corners.
- Prevent unfair pipe generation (gaps must stay in playable bounds).
- Keep game states clear:
  - Start screen
  - Playing
  - Mod menu pause
  - Game over
  - Win screen
- Required functionality:
  - Move player (mouse or flap mode).
  - Spawn and move pipe segments.
  - Detect collisions.
  - Score gaps passed.
  - Support difficulty + game modes.
  - Play music and show HUD.

#### Script structure

- Single file implementation: `main.py`.
- Main elements:
  - Global constants/config dictionaries (`DIFFICULTIES`, `THEMES`, gameplay constants).
  - Helper functions (`get_asset_path`, `load_music`, collision helpers, drawing).
  - `PipeSegment` class for obstacle behavior/data.
  - `run_game()` main loop for events, updates, rendering.

#### Input-output relationships

- **Input:** keyboard/mouse events from `pygame.event.get()` and mouse position.
- **Processing:** update control mode, cube position/velocity, segment movement/spawn, collision and score logic.
- **Output:** rendered graphics (`screen.blit`, `pygame.draw.*`) + music playback (`pygame.mixer.music`).

Examples:

- Mouse Y changes → cube target Y updates → cube glides.
- Key press in flap mode → upward impulse (`FLAP_IMPULSE`) → cube jumps.
- Cube touches wall rects → `game_over = True` → game-over overlay shown.

### 🎨 Two Proposed Solutions – Storyboards / Screen Designs (2B.P3, 2B.M2)

#### Proposed Solution A (implemented): Mouse/Flap Pipe Runner

Screens:

1. **Start Screen**
   - Title, controls hint, difficulty select, mode select, theme select.
2. **Gameplay Screen**
   - Scrolling pipes, cube, score HUD, timer (time attack), slow meter.
3. **Mod Menu Overlay**
   - Pause + toggles (hitbox, control mode, theme, ghost, fullscreen, volume, FPS).
4. **Game Over Screen**
   - Failure message + retry prompt.
5. **Win Screen**
   - Success message + replay prompt.

Functions used:

- Event/input: `run_game()` event loop branches.
- Spawn/update: `spawn_segment()`, `PipeSegment.move()`.
- Collision: `PipeSegment.collides_with_cube()`, `rounded_rect_collides_rect()`.
- Rendering: `draw_cube_with_face()`, pipe/HUD draw code in `run_game()`.

Constraints/barriers:

- Screen size and HUD area reduce vertical play area.
- Pygame is 2D only (no built-in scene system).
- Must remain suitable for ages 7+ (no complex UI).
- Performance on lower-end school devices.

#### Proposed Solution B (alternative design): Lane-Based Gap Runner

Screens:

1. **Menu Screen** (Play, Difficulty, Theme)
2. **Lane Gameplay** (3 fixed lanes, keyboard lane-switch left/right)
3. **Pause Overlay**
4. **Game Over / Win**

Functions that would be used:

- `handle_input()` for lane switch.
- `update_obstacles()` for lane obstacle movement.
- `check_lane_collision()` for collision.
- `draw_scene()` for rendering.

Constraints/barriers:

- Simpler control but less smooth feeling.
- Less expressive than free Y-position glide.
- Easier to implement but potentially less engaging.

#### Screen navigation diagram (2B.M2)

- `Start Menu` -> `Gameplay`
- `Gameplay` -> `Mod Menu` (TAB)
- `Mod Menu` -> `Gameplay` (TAB)
- `Gameplay` -> `Game Over` (collision or timer zero)
- `Gameplay` -> `Win` (goal reached)
- `Game Over` -> `Gameplay` (SPACE retry)
- `Win` -> `Gameplay` (SPACE replay)

#### Data structures used (2B.M2)

- **Scalars:** `score`, `cube_y`, `cube_velocity_y`, `elapsed_time`, booleans (`game_over`, `won`).
- **Lists:** `segments` (`PipeSegment` objects), `ghost_data` and `current_run_recording` (time-position tuples).
- **Dictionaries:** `DIFFICULTIES`, `THEMES` for configurable settings.
- **Object/class:** `PipeSegment` with `x`, `width`, gap geometry, score flags.

#### Data validation and error handling (2B.M2)

- Position clamping:
  - Cube Y clamped to playable bounds.
  - Gap center constrained to valid range.
- Defensive timing:
  - `dt_sec` minimum fallback avoids divide/update instability.
- Audio safety:
  - `load_music()` checks file exists and catches `pygame.error`.
  - Win-state music stop wrapped in `try/except`.
- Collision fallback:
  - Rounded collision function falls back to rectangular collision for invalid radius.

#### Controls and events mapping (2B.M2)

- Mouse move -> cube glide target.
- `SPACE`/`ENTER`/click on start -> begin run.
- `1/2/3` -> difficulty.
- `4/5/6` -> mode (normal/time attack/flappy).
- `TAB` -> mod menu open/close.
- `H/C/G/F/R/Q/A/Z/X/P` in mod menu -> feature toggles/settings.
- `ESC` -> quit.
- `F11` -> fullscreen toggle.

#### Evaluation of storyboard solutions (2B.M2)

- **Solution A strengths:** richer gameplay, two control styles, replay value from modes/mods, already implemented and tested.
- **Solution A weaknesses:** higher code complexity and more states to maintain.
- **Solution B strengths:** easy for younger users, very simple logic/testing.
- **Solution B weaknesses:** reduced challenge depth and less replay variety.
- **Chosen option:** Solution A because it better meets the project goal of engaging arcade gameplay while staying accessible.

### 📦 Asset List (2B.P3)

#### Variables (sample key state table)

| Name | Type | Purpose | Initial Value |
|---|---|---|---|
| `score` | `int` | Number of gaps successfully passed | `0` |
| `cube_x` | `float` | Fixed player horizontal position | `100.0` |
| `cube_y` | `float` | Player vertical position | center-derived |
| `cube_velocity_y` | `float` | Vertical speed in flap mode | `0.0` |
| `segments` | `list[PipeSegment]` | Active obstacle segments | `[]` |
| `game_over` | `bool` | Loss state flag | `False` |
| `won` | `bool` | Win state flag | `False` |
| `difficulty` | `str` | Difficulty profile key | `"medium"` |
| `game_mode` | `str` | Current mode | `"normal"` |
| `time_attack_remaining` | `float` | Countdown timer in time attack | `60.0` |
| `theme` | `str` | Active visual theme | `"classic"` |
| `slow_charge` | `float` | Slow-motion meter amount | `0.0` |
| `show_ghost` | `bool` | Ghost replay display toggle | `False` |

#### Controls & media

| Category | Item | Use |
|---|---|---|
| Input | Mouse movement | Glide control |
| Input | Mouse click | Start game |
| Input | `SPACE` / `ENTER` | Start/retry and slow-motion hold |
| Input | Number keys `1-6` | Difficulty/mode selection |
| Input | `TAB` | Mod menu |
| Input | `F11`, `ESC`, `T` | Fullscreen, quit, cursor toggle |
| Input | `H C G F R Q A Z X P` | Mod menu controls |
| On-screen text | Title/HUD/menu text | Guidance, score, mode, status |
| Sound | `music.mp3` | Optional looping background music |
| Image files | None required | Game uses drawn shapes (Pygame primitives) |

### 💻 Pseudo Code & Flowchart (2B.P3, 2B.M2)

#### Pseudo code (key procedures)

```text
START program
  initialise pygame, mixer, window, fonts
  load music if file exists
  set initial game state variables

  WHILE running:
    dt = clock.tick(FPS_TARGET) / 1000
    read events
      if quit or ESC -> running = false
      if start screen and start input -> reset run state
      if gameplay and TAB -> toggle mod menu
      if flap mode and key press -> apply flap impulse
      if mod menu key -> toggle selected option

    IF start screen:
      draw title/options
      continue loop

    IF active gameplay (not paused/game over/won):
      update timers and recordings
      update speed from difficulty + score
      process slow-motion
      update cube movement (mouse smooth or flap physics)
      build cube rect
      FOR each pipe segment:
        move segment left
        if collision -> game over
        if passed correctly -> score++
      remove off-screen segments
      spawn new segment if needed

    draw world, HUD, cube, optional ghost/hitbox
    draw overlays (mod menu / game over / win)
    display frame

  quit pygame
END program
```

#### Flowchart (text representation)

```text
[Start]
   |
   v
[Initialise pygame/state]
   |
   v
[Main loop]
   |
   v
[Handle input/events] --quit--> [Exit]
   |
   +--start screen?--> [Draw start] --> [Main loop]
   |
   +--active gameplay?--> [Update physics/timers]
   |                         |
   |                         v
   |                     [Collision?]--yes-->[Game over state]
   |                         |
   |                         no
   |                         v
   |                     [Scored? update score/win]
   |
   v
[Render frame + overlays]
   |
   v
[Main loop]
```

#### Pre-defined functions/subroutines list (2B.P3)

| Function/Subroutine | Parameters | Return | Purpose |
|---|---|---|---|
| `get_asset_path` | `filename` | `str` path | Resolve file path next to script |
| `load_music` | `volume=0.6` | `bool` | Load/play music safely |
| `_circle_rect_overlap` | `cx, cy, radius, rect` | `bool` | Circle-rect overlap helper |
| `rounded_rect_collides_rect` | `cube_rect, radius, wall_rect` | `bool` | Rounded hitbox collision check |
| `spawn_segment` | `x, play_top, play_bottom, ...` | `PipeSegment` | Create random pipe segment |
| `draw_cube_with_face` | `surface, rect, theme_dict, ghost_alpha` | `None` | Draw player/ghost cube |
| `run_game` | none | `None` | Main loop and game controller |
| `PipeSegment.move` | `dx` | `None` | Move segment |
| `PipeSegment.collides_with_cube` | cube + bounds | `bool` | Collision with walls |
| `PipeSegment.is_in_gap` | `cube_rect` | `bool` | Check if cube center in gap |
| `PipeSegment.is_passed_cube` | `cube_x` | `bool` | Check score pass condition |

### 🧪 Test Plan & Test Data (2B.M2)

#### Planned tests

| Test ID | Description | Type | Expected Result |
|---|---|---|---|
| T01 | Program starts with no syntax/import errors | Compilation | Game window opens successfully |
| T02 | Start game from menu via SPACE | Functional | Transitions to gameplay |
| T03 | Mouse glide movement | Functional | Cube follows mouse smoothly |
| T04 | Flap mode key press | Functional | Cube jumps up with impulse |
| T05 | Pipe collision | Logic | Game over triggers on impact |
| T06 | Pass through gap | Logic | Score increments by 1 once |
| T07 | Difficulty changes (`1/2/3`) | Functional | Speed/gaps change by profile |
| T08 | Time attack timeout | Boundary/time | Game over when timer reaches 0 |
| T09 | Win at goal score | Boundary/logic | Win overlay appears at target |
| T10 | Music file missing | Error handling | No crash, game still runs |
| T11 | Fullscreen toggle (`F11`) | Functional | Switches mode and keeps gameplay |
| T12 | Mod menu pause (`TAB`) | Functional | Gameplay pauses/resumes correctly |

#### Test data (valid, invalid, boundary)

| Input / Variable | Valid Test Data | Invalid/Edge Data | Expected Output |
|---|---|---|---|
| Difficulty key | `1`, `2`, `3` | Other keys | Only mapped keys change difficulty |
| Mode key | `4`, `5`, `6` | Other keys | Only mapped keys change mode |
| Music file | `music.mp3` exists | Missing/corrupt file | No crash, returns `False` in loader |
| Time attack timer | `>0` | `<=0` boundary | Ends run at zero or less |
| Slow meter | `0.0` to `2.0` | Underflow attempt | Clamped to `0.0` minimum |
| Cube position | Within play bounds | Above HUD / below bottom | Clamped in bounds |

### 🔀 Alternative Solutions (2B.M2, 2B.D2)

#### Possible alternative technologies

- Scratch
- Unity (C#)
- Godot (GDScript/C#)
- JavaScript + Phaser

#### Why alternatives were rejected

- **Scratch:** very accessible but limited control for this style of smooth physics and modular feature growth.
- **Unity/Godot:** powerful but over-scoped for a small 2D coursework game and steeper setup for timeline.
- **Phaser (JS):** good for web, but requires browser/deployment workflow beyond current classroom setup.
- **Chosen stack (Python + Pygame):** fastest route to a complete, testable desktop prototype with readable code.

### ✅ Justification for Design Decisions (2B.D2)

#### Why this chosen design fits the brief

- Meets age 7+ accessibility with simple controls and clear feedback.
- Includes increasing challenge and replayability (difficulty, modes, ghost replay, slow motion).
- Uses clear game states and modular functions for maintainability.
- Runs on standard PC hardware with minimal dependencies.

#### Constraints and how design addresses them

| Constraint | Impact | Design Response |
|---|---|---|
| Time deadline | Limited development/testing window | Single-file architecture with focused feature set |
| Target age (7+) | Must be understandable and non-complex | Simple controls, readable HUD text, immediate retry |
| Hardware/software | School/home PCs may vary | Pygame + delta-time motion for stable behavior |
| Content safety | Must be age-appropriate | Non-violent abstract visuals and neutral language |
| Technical risk | Audio/assets may fail | File checks and try/except safety in audio loading |

---

## AI Evidence Status Snapshot

Based on your current project, most technical evidence can now be referenced directly from this `README.md`.
=
