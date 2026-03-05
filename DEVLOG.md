# Cube Jump — Development Log

A devlog for the 2D pygame game **Cube Jump**: from a blank window to a full game where you glide a cube with a face through a scrolling pipe to 999 points (might change high score, over estimating my skill on this game).

---

## Version 1 — Initialising Python and Pygame

**File:** `versions/v01_initialise_pygame.py`

We start from zero: a Python script that initialises pygame and opens a window.

- **Pygame init:** `pygame.init()` so we can use display, events, and (later) mixer.
- **Display:** A single window, 900×600, with a title.
- **Game loop:** A `while running` loop that keeps the window open and responsive.
- **Events:** Handle `pygame.QUIT` (window close) and `pygame.KEYDOWN` for ESC so the player can exit.
- **Update:** `pygame.display.flip()` so something is drawn (we fill the screen with a dark background so it’s not black-by-default).
- **Cleanup:** `pygame.quit()` when the loop ends.

No game objects yet—just a stable foundation that closes properly and doesn’t freeze.

---

## Version 2 — Drawing the Cube

**File:** `versions/v02_draw_cube.py`

We add the thing the player will control: a cube.

- **Constants:** Window size and a single `CUBE_SIZE` so the cube is easy to tweak.
- **Position:** Cube is drawn at a fixed position (e.g. left side, vertically centred in the play area).
- **Drawing:** A simple rectangle with `pygame.draw.rect()`—colour and size only, no face yet.
- **Play area:** We treat the bottom part of the screen as “play area” so the cube isn’t under the future HUD.

The game still has no input or movement; the cube is static. This step confirms that drawing and the game loop work together.

---

## Version 3 — Mouse Control (Glide)

**File:** `versions/v03_mouse_control.py`

The cube should follow the mouse so the player can “glide” through the pipe.

- **Mouse input:** `pygame.mouse.get_pos()` each frame to get cursor position.
- **Vertical only:** We only use the Y coordinate so the cube moves up/down; X can stay fixed (e.g. left side of the pipe).
- **Clamping:** Cube Y is clamped so it stays inside the play area (below the HUD, above the bottom).
- **Smoothing (optional in v03):** We can either snap the cube to the mouse or start smoothing (e.g. lerp) so it feels like “gliding.” For the version file we use simple follow; smoothing comes with delta time later.

Now the player can move the cube with the mouse—the core input for the whole game.

---

## Version 4 — Pipe and Gaps (Scrolling)

**File:** `versions/v04_pipe_scrolling.py`

We add the pipe: segments with gaps that scroll from right to left.

- **Pipe segment:** A simple representation: x position, width, gap centre Y, gap height. Each segment is a vertical strip with a “hole” (gap) the cube must pass through.
- **Drawing:** For each segment we draw two rectangles (top wall and bottom wall), leaving the gap empty.
- **Scrolling:** Each frame we move every segment left by a fixed amount (pixels per frame for now; we’ll switch to per-second in v07).
- **Spawning:** When the rightmost segment has moved far enough left, we spawn a new segment at the right edge of the screen with a random gap position and height.
- **Removal:** Segments that move fully off the left side are removed from the list.

No collision yet—the cube and pipe are independent. This version proves that the pipe looks right and scrolls smoothly.

---

## Version 5 — Collision, Scoring, Game Over

**File:** `versions/v05_collision_scoring.py`

We add the core rules: hit the wall = game over; pass through a gap = score.

- **Collision:** For each segment we check if the cube’s rectangle overlaps the “wall” parts (top or bottom) and not the gap. If it does, we set `game_over = True`.
- **Scoring:** When the cube is inside the gap (centre in gap) we mark “was in gap.” When the segment has fully passed the cube (segment’s right edge is left of the cube) and we were in the gap, we add 1 point and mark that segment as scored so we don’t double-count.
- **Game over state:** When `game_over` is True we stop moving the cube and pipe, show a simple “Hit the pipe” message, and allow SPACE to reset and play again (reset score, cube position, clear segments).

Now the game is playable: avoid walls, pass through gaps, and see a score.

---

## Version 6 — HUD, Difficulty, Goal (999), Secret Surprise

**File:** `versions/v06_hud_goal_surprise.py`

We add the HUD, difficulty ramp, win condition, and the “secret surprise” reward.

- **HUD:** A bar at the top of the screen showing “Gaps: X / 999” so the player always knows progress. We use a simple font and a line to separate HUD from play area.
- **Difficulty:** Scroll speed increases with score (e.g. `base_speed + score * increase`). We cap this at score 50 so it doesn’t get harder after 50 points (`min(score, 50)`).
- **Goal:** The target is 999 points. When `score >= 999` we set `won = True`.
- **Secret surprise:** When the player wins we show a dedicated screen: “SECRET SURPRISE!”, “You reached 999 gaps! You’re a champion.”, and “Press SPACE to play again.” Optionally we stop the music here for emphasis.
- **Retry after win:** Same as after game over: SPACE resets game state (score, cube, segments, `game_over`, `won`) so they can play again.

The game now has a clear goal, feedback, and a reward for reaching 999.

---

## Version 7 — FPS-Independent Physics (Delta Time)

**File:** `versions/v07_delta_time.py`

We tie all movement to time instead of frame count so the game behaves the same at any FPS.

- **Delta time:** Each frame we compute `dt_sec = clock.tick(FPS_TARGET) / 1000.0` (with a small minimum to avoid division issues). All movement uses “per second” values multiplied by `dt_sec`.
- **Pipe scroll:** `move = scroll_speed_per_second * dt_sec`; segments move by `-move` each frame.
- **Cube smoothing:** The cube’s Y movement toward the mouse target uses a per-second smoothing factor (e.g. `cube_y += (target_y - cube_y) * min(1.0, smooth_speed * dt_sec)`). So on a slow PC (low FPS) or fast PC (high FPS), one second of real time gives the same amount of movement.
- **Constants:** Speeds are defined in “per second” (e.g. pixels per second, “smooth factor” per second). We keep a target FPS for `clock.tick()` only to limit CPU usage; gameplay no longer depends on that number.

The game is now fair and consistent regardless of monitor refresh rate or machine speed.

---

## Version 8 — Final Polish: Cube Face, Music, HUD Text

**File:** `versions/v08_final.py`

We add character to the cube, audio, and a bit of extra feedback.

- **Cube face:** Instead of a plain rectangle we draw a “cube with a face”: same rect with rounded corners, two eyes (white + dark pupils), and a smile (arc). This gives the cube a clear identity and makes the game more memorable.
- **Music:** We use `pygame.mixer` and look for an MP3 file (e.g. `music.mp3`). In `main.py` the file is in the game folder; in `versions/v08_final.py` the path points to the project root (parent of `versions/`) so the same `music.mp3` works when run from either place. If the file is missing we skip without crashing.
- **HUD hint:** We add a short hint in the HUD when playing: “Glide with mouse!” so new players know the control without reading docs.
- **Cleanup:** Any small tweaks (colours, font sizes, messages) to match the design doc.

This is the version that matches the current `main.py`: full gameplay, FPS-independent, with face, music, and the 999-gap secret surprise.

---

## Summary Table

| Version | Focus |
|--------|--------|
| v01 | Pygame init, window, event loop, quit |
| v02 | Draw a static cube |
| v03 | Cube follows mouse (glide) |
| v04 | Pipe segments with gaps, scrolling |
| v05 | Collision, scoring, game over, retry |
| v06 | HUD, difficulty cap at 50, goal 999, secret surprise |
| v07 | Delta time — FPS-independent physics |
| v08 | Cube face, music (MP3), HUD hint, final polish |

---

## How to Run the Versions

From the project folder:

```bash
python versions/v01_initialise_pygame.py
python versions/v02_draw_cube.py
# ... and so on through v08_final.py
```

The main game (current state) is still:

```bash
python main.py
```

`main.py` is equivalent to v08 with the same feature set; the version files are a step-by-step reconstruction of how the game could have been built from the beginning.
