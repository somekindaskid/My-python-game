# Cube Jump — Every Version & How It Works

I built this game step by step and saved a snapshot after each big change. Here’s every version, what it does, what I actually did, and the (sometimes annoying) problems I ran into along the way.

---

## Version 1 — `v01_initialise_pygame.py`

**What it does:** Opens a window. That’s it. Dark grey background, 900×600. You can close the window or press ESC to quit. No cube, no pipe, no game yet.

**What I did:** Set up the boring-but-necessary stuff: `pygame.init()`, create the display, a `while running` loop, handle `QUIT` and `KEYDOWN` for ESC, `screen.fill()` and `display.flip()`, then `pygame.quit()` when you leave. I also added `clock.tick(60)` so the loop doesn’t max out the CPU.

**Problems I had:** First time I ran it the window opened and immediately closed. I’d forgotten the event loop—Python just hit the end of the script and exited. Took me a second to realise I needed a loop that kept running until the user quit. Then I had the opposite issue: I closed the window and the process kept running because I wasn’t checking for `pygame.QUIT`. Felt dumb but fixed it.

---

## Version 2 — `v02_draw_cube.py`

**What it does:** Same window, but now there’s a blue rounded rectangle (the cube) on the left side, vertically centred in the play area. A thin line separates the top “HUD” zone from where the cube lives. Still no movement.

**What I did:** Defined `CUBE_SIZE`, `HUD_HEIGHT`, and the play area (between HUD and bottom of screen). Cube position is fixed: x=100, y = centre of play area. I draw the cube with two `pygame.draw.rect()` calls—one filled, one outline—and use `border_radius=6` so it’s not a harsh square.

**Problems I had:** I originally drew the cube at (0, 0) and half of it was under the title bar / felt wrong. I had to sit down and decide where the “game” area actually was. I also messed up the centering math at first—forgot to subtract half of `CUBE_SIZE` from the centre y, so the cube was sitting too low. Quick fix once I drew it on paper.

---

## Version 3 — `v03_mouse_control.py`

**What it does:** The cube now follows your mouse up and down. Move the cursor and the cube glides to match. It can’t go above the play area or below the bottom. Horizontal position stays fixed.

**What I did:** Every frame I get `pygame.mouse.get_pos()`, use only the Y value, and convert it so the cube is “centred” under the cursor (mouse_y - CUBE_SIZE // 2). Then I clamp that to `[play_top, play_bottom - CUBE_SIZE]` so the cube never leaves the visible play area.

**Problems I had:** At first I didn’t clamp. If you moved the mouse above the window the cube tried to go to negative y and basically vanished. Same thing at the bottom—cube went off screen. Took one playtest to notice. Then I had a bug where I was still using integer division for cube_y in one place and a float in another and got a type error when passing to `Rect`. Small thing but annoying. Also the cube felt really twitchy because it snapped to the mouse every frame—I left it like that for v03 and only added smoothing later (v07) when I had delta time.

---

## Version 4 — `v04_pipe_scrolling.py`

**What it does:** The pipe appears. It’s made of segments: each segment is a vertical strip with a gap (hole) in the middle. Segments scroll from right to left. The cube and pipe don’t interact yet—you can fly through walls and nothing happens. It’s just to get the pipe on screen and moving.

**What I did:** I represented each segment as a dict with x, width, gap_center_y, gap_half_height. Each frame I subtract a constant (e.g. 4 pixels) from every segment’s x. I draw two rectangles per segment—one for the wall above the gap, one for the wall below—so the gap is the “empty” bit in the middle. When the rightmost segment is far enough left I spawn a new one at x = WINDOW_W with a random gap position and height (within limits so the gap doesn’t go off screen). I also remove segments that have scrolled fully off the left (x + width < 0).

**Problems I had:** First version of the spawn logic made segments overlap or have huge gaps. I was spawning every frame when the last segment’s x was less than something—forgot to add a minimum distance between segments, so sometimes two segments were on top of each other. Took a bit to get the “when to spawn” condition right. I also had the gap centre calculated wrong once so the gap could be partly above play_top or below play_bottom—had to clamp the random gap centre so the whole gap stays in bounds. And I kept mixing up “gap_center_y” and “gap_half_height” when drawing—drew the wrong rectangles and the gap was in the wrong place. Debugging with print statements on the first segment’s values fixed that.

---

## Version 5 — `v05_collision_scoring.py`

**What it does:** Real game logic. If the cube hits the pipe wall (top or bottom of a segment), it’s game over and you see “Oops! Hit the pipe. Press SPACE to retry.” If you pass through a gap (cube centre was in the gap when the segment passed you), you get +1 point. SPACE resets everything so you can play again.

**What I did:** For each segment I check: does the cube’s rect overlap this segment in x? If yes, is the cube in the gap (centre y between gap top and bottom) or in the wall? If it’s in the wall → set game_over. I also track “was_in_gap” per segment: when the cube is overlapping the segment and its centre is in the gap, I set that. When the segment has fully passed the cube (segment’s right edge < cube’s left) and we had was_in_gap and haven’t scored this segment yet, I add 1 to score and mark the segment as scored so we don’t double-count. When game_over is true I stop updating cube/pipe and show an overlay with the message; SPACE clears state and starts fresh.

**Problems I had:** Biggest headache was scoring. I was giving a point as soon as the cube entered the gap, so you got like 3 points per segment because the cube overlaps for several frames. I had to change it to “only give the point when the segment has completely passed the cube” and “only if we were ever in the gap during that overlap.” Took a while to get the logic right. I also had a bug where I was checking collision after moving the segment, but I was using the cube’s rect from the start of the frame—so sometimes the segment “jumped” through the cube in one frame and no collision was detected. I made sure movement and collision use the same cube position. Oh, and I forgot to reset “was_in_gap” and “scored” when spawning new segments at first—I was reusing the same dict keys and had to make sure every new segment gets fresh flags.

---

## Version 6 — `v06_hud_goal_surprise.py`

**What it does:** HUD at the top shows “Gaps: X / 999” so you always know your progress. The pipe scrolls faster as you score more, but the difficulty stops increasing after 50 points (so it doesn’t get impossible). If you reach 999 gaps you get a “SECRET SURPRISE!” screen that says you’re a champion and you can press SPACE to play again.

**What I did:** I draw the HUD text every frame with the current score and the goal (999). Scroll speed is now something like base + min(score, 50) * increase so it caps. When score >= 999 I set a “won” flag and show a full-screen overlay with the surprise message and the “Press SPACE to play again” line. SPACE now resets both game_over and won states so you can retry after either losing or winning.

**Problems I had:** I initially let the speed increase forever. By 200 points it was unplayable. Playtesting (and a friend complaining) made me add the cap at 50. I also had the “won” state show up for one frame then disappear because I was resetting something in the wrong order when handling SPACE—had to be careful that “won” and “game_over” are both reset and that we don’t accidentally add score or move the cube in the same frame we detect win. Another dumb one: I typed the goal as 99 instead of 999 and didn’t notice until I was writing the surprise text. And the HUD looked cramped until I added a bit of spacing and the “Glide with mouse!” hint so it wasn’t just a number.

---

## Version 7 — `v07_delta_time.py`

**What it does:** Same game as v06, but all movement is tied to time instead of frames. So if you have a slow PC (30 FPS) or a fast one (144 FPS), the pipe scrolls and the cube glides at the same “real” speed. The game feels the same on any machine.

**What I did:** I use `clock.tick(FPS_TARGET)` and then get `dt_sec = clock.tick(...) / 1000.0` (with a small minimum so we never divide by zero). Every speed is now “per second”: e.g. scroll_speed in pixels per second. Each frame I do move = scroll_speed * dt_sec and move the pipe by that much. For the cube I wanted it to smoothly follow the mouse, so I do something like cube_y += (target_y - cube_y) * min(1.0, smooth_speed * dt_sec) so the cube lerps toward the mouse with a time-based factor. That way one second of real time always gives the same amount of “catching up” regardless of FPS.

**Problems I had:** At first I left everything in “pixels per frame.” On my 60 Hz monitor it was fine; when I uncapped the frame rate the pipe flew across the screen and the cube was super sensitive. Took me a minute to remember delta time from other projects. I had to go through every place that moved something and multiply by dt_sec. I also had a bug where I was still adding “scroll per frame” in one place and “scroll * dt” in another and the pipe stuttered. Once everything was consistently in “per second” it was fine. I also had to guard against dt_sec being 0 or negative (e.g. if the system clock does something weird) so I clamp it to a tiny positive value.

---

## Version 8 — `v08_final.py`

**What it does:** The full game as it is now. Same as v07 but the cube has a face (eyes and a smile), background music plays from an MP3 file if it’s in the project folder, and the HUD has the “Glide with mouse!” hint. Reaching 999 still gives the secret surprise; music stops when you win.

**What I did:** I replaced the plain blue rect with a “draw_cube_with_face” function: same rounded rect, then two small ellipses for eyes (white + dark pupils) and an arc for a smile. For music I use pygame.mixer, look for a file (e.g. music.mp3) next to the project—when the script is in `versions/` I look in the parent folder so the same music file works from the main folder or from versions. If the file isn’t there I just skip loading so the game doesn’t crash. On win I stop the music and show the surprise screen.

**Problems I had:** The face looked weird at first—eyes too big, smile in the wrong place. I tweaked the offsets and sizes until it looked like a face and not a blob. For the music I first used a path relative to the current working directory, so when I ran `python versions/v08_final.py` from the project root it tried to load `versions/music.mp3` and failed. I switched to resolving the path relative to the script file (or the project root when in versions/) so it finds the MP3 no matter where you run the command from. Someone also reported pygame.mixer crashing on their machine when the MP3 was missing—I wrapped the load/play in a try/except and only play if the file exists and loads without error.

---

## Quick reference

| Version | File | What you get |
|--------|------|----------------|
| 1 | `v01_initialise_pygame.py` | Blank window, quit on close/ESC |
| 2 | `v02_draw_cube.py` | Static cube on screen |
| 3 | `v03_mouse_control.py` | Cube follows mouse Y |
| 4 | `v04_pipe_scrolling.py` | Pipe with gaps scrolling left |
| 5 | `v05_collision_scoring.py` | Collision, score, game over, retry |
| 6 | `v06_hud_goal_surprise.py` | HUD, difficulty cap, 999 goal, surprise screen |
| 7 | `v07_delta_time.py` | FPS-independent movement |
| 8 | `v08_final.py` | Cube face, music, full game |

Run any of them from the project folder, e.g.:

```bash
python versions/v01_initialise_pygame.py
python versions/v08_final.py
```

The main game (same as v08) is still `python main.py`.
