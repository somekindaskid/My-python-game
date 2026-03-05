# Cube Jump

A 2D game made in Python with pygame for PC. Control a cube with a face through a scrolling pipe using your mouse.

**Continuing the project later (e.g. from USB)?** See [CONTINUE_HERE.md](CONTINUE_HERE.md) for what’s implemented and where to pick up.

For a step-by-step development story and runnable versions from “blank window” to full game, see [VERSIONS_README.md](VERSIONS_README.md) (version-by-version + fake dev problems), [DEVLOG.md](DEVLOG.md), and the `versions/` folder (e.g. `python versions/v01_initialise_pygame.py` through `v08_final.py`).

## How to play

- **Control:** Move your mouse up and down to glide the cube through the pipe (or switch to **Flap** mode in the mod menu and use any key to jump, Flappy Bird style).
- **Goal:** In **Normal** mode, pass through **999 gaps**; in **Time attack**, get **30 gaps in 60 seconds**.
- **Rules:** Slide smoothly into each gap; hitting the wall ends the run. In time attack, running out of time also ends the run.
- **Difficulty:** Scroll speed increases as you score (capped after 50 gaps). Choose **Easy**, **Medium**, or **Hard** on the start screen (see below).

## Time attack (start screen)

Press **5** on the start screen to select **Time attack** mode. You have **60 seconds** to pass through **30 gaps**. A countdown timer appears in the HUD. Win by reaching 30 gaps before time runs out. Press **4** for Normal (endless to 999) mode.

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

## Difficulty (start screen)

On the start screen, pick a difficulty before you play:

- **Easy** (press **1**): Slower scroll, more space between pipes, larger gaps. Best for learning the game.
- **Medium** (press **2**): Default balance of speed and gap size.
- **Hard** (press **3**): Faster scroll, pipes closer together, smaller gaps.

Your choice is shown under the title; press **SPACE** or click to start.

## Mod menu (TAB)

Press **TAB** during gameplay to open the mod menu. The game pauses while the menu is open. Press **TAB** again to close and resume.

- **Show hitbox (H):** Toggle ON to see the cube’s real collision box (green outline).
- **Control (C):** Switch between **Mouse** and **Flap** (any key to jump).
- **Theme (G):** Cycle Classic / Neon / Minimal.
- **Fullscreen (F):** Toggle fullscreen.
- **Ghost replay (R):** Show last run as a semi-transparent ghost cube.
- **Music (Q/A):** Increase / decrease music volume.
- **SFX (Z/X):** Increase / decrease SFX volume (for future sounds).

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
- **4 / 5** on start screen: Normal / Time attack mode  
- **G** on start screen: cycle theme (Classic / Neon / Minimal)  
- **SPACE** (or **Enter**) or click on start screen: play  
- **SPACE** after game over or win: play again  
- **TAB:** open/close mod menu  
- **F11** or **F** (in mod menu): fullscreen  
- **T:** hide/show cursor  
- **Flap mode:** any key except ESC or TAB to jump  

## Technical notes

- All movement and scrolling use **delta time** (per-second speeds), so gameplay is the same at any frame rate (e.g. 30, 60, 120+ FPS).
- The HUD at the top shows how many gaps you’ve passed and the 999 goal.
- Reaching 999 gaps triggers the in-game secret surprise.
