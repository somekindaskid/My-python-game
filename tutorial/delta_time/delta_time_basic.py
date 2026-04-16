import pygame

"""
Delta time tutorial
-------------------

This file shows a very small example of what "delta time" is and how to use it.

Goal:
- Make a square move across the screen at a constant speed,
  even if the FPS (frames per second) changes.

Key idea:
- Instead of moving by a fixed number of pixels every frame
  (for example: x += 5),
  we move by "speed_per_second * dt", where:
    - speed_per_second is in pixels per SECOND
    - dt is how many SECONDS passed since the last frame

So the position change per frame is:
    delta_x = speed_per_second * dt
and dt comes from pygame's clock:
    dt = clock.tick(FPS_TARGET) / 1000.0
"""


# Window size (just some simple numbers)
WINDOW_W, WINDOW_H = 800, 600

# This is only the *target* FPS. The real FPS can be higher or lower.
FPS_TARGET = 60

# We want the square to move 250 pixels per second horizontally.
SPEED_X_PER_SECOND = 250.0


def main():
    # Initialize pygame and create a window.
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Tutorial: Basic Delta Time")

    # This clock gives us the time between frames.
    clock = pygame.time.Clock()

    # Our square will start near the left edge, vertically centered.
    x = 50.0
    y = WINDOW_H / 2 - 25
    size = 50

    running = True
    while running:
        # 1) Get delta time (dt)
        # clock.tick(FPS_TARGET) returns milliseconds since last call.
        # We divide by 1000.0 to convert ms -> seconds.
        dt = clock.tick(FPS_TARGET) / 1000.0

        # Sometimes dt can be 0 (or very small) if the OS hiccups.
        # We can clamp it to a tiny positive value if we want.
        if dt <= 0:
            dt = 0.001

        # 2) Handle events (close window, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 3) Update game state using dt
        #
        # We want a constant horizontal speed, independent of FPS.
        # So we move by (speed * dt) each frame.
        x += SPEED_X_PER_SECOND * dt

        # If the square goes off the right side, wrap it around to the left.
        if x > WINDOW_W:
            x = -size

        # 4) Draw everything
        screen.fill((24, 28, 36))  # dark background

        # Draw a simple blue square.
        pygame.draw.rect(screen, (70, 130, 200), (int(x), int(y), size, size))

        # Optional text: show dt on screen so you can see it changing.
        font = pygame.font.Font(None, 28)
        dt_text = font.render(f"dt: {dt:.4f} seconds", True, (220, 220, 230))
        fps_text = font.render(f"FPS (approx): {clock.get_fps():.1f}", True, (220, 220, 230))
        screen.blit(dt_text, (20, 20))
        screen.blit(fps_text, (20, 50))

        # Flip the frame to the screen.
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

