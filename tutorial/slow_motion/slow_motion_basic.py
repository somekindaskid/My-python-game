import pygame

"""
Slow motion tutorial
--------------------

This file shows how to:
- Use delta time (dt) to move things at a constant speed.
- Add a "time scale" value to slow the whole game down (slow motion).

Key ideas:
1) Delta time (dt) is the time in SECONDS between frames.
   We get it from pygame's clock:
       dt = clock.tick(FPS_TARGET) / 1000.0

2) Normally we update movement like this:
       position += speed_per_second * dt

3) To add slow motion, we add a "time_scale" multiplier:
       effective_dt = dt * time_scale
       position += speed_per_second * effective_dt

   - If time_scale = 1.0  -> normal speed
   - If time_scale = 0.5  -> everything is half speed
   - If time_scale = 0.2  -> super slow motion

In this example:
- Press and HOLD SPACE to slow time down.
"""

# Window size
WINDOW_W, WINDOW_H = 800, 600

# Target FPS for the display (logic still uses dt)
FPS_TARGET = 60

# Speeds in pixels per second
SPEED_X_PER_SECOND = 250.0  # how fast the square moves sideways

# Time scale values
NORMAL_TIME_SCALE = 1.0
SLOW_TIME_SCALE = 0.25  # 25% speed when slow motion is active


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Tutorial: Slow Motion with Delta Time")
    clock = pygame.time.Clock()

    # Start our square near the left, in the middle vertically.
    x = 50.0
    y = WINDOW_H / 2 - 25
    size = 50

    running = True
    while running:
        # 1) Get raw delta time (dt) in seconds.
        dt = clock.tick(FPS_TARGET) / 1000.0
        if dt <= 0:
            dt = 0.001

        # 2) Handle events (quit, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 3) Decide time_scale based on input.
        #
        # Here we keep it simple:
        # - If SPACE is held: slow motion
        # - Else: normal speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            time_scale = SLOW_TIME_SCALE
        else:
            time_scale = NORMAL_TIME_SCALE

        # Combine dt with time_scale to get the "effective" dt
        effective_dt = dt * time_scale

        # 4) Update the square's position using effective_dt,
        # so it automatically respects slow motion.
        x += SPEED_X_PER_SECOND * effective_dt

        # Wrap around the screen when it goes too far right.
        if x > WINDOW_W:
            x = -size

        # 5) Draw everything
        screen.fill((15, 18, 26))

        # Use a different color when slow motion is active
        if time_scale < 1.0:
            color = (200, 80, 120)  # reddish when slowing down
        else:
            color = (70, 130, 200)  # blue when normal

        pygame.draw.rect(screen, color, (int(x), int(y), size, size))

        # 6) Draw some helpful text on screen
        font = pygame.font.Font(None, 28)
        dt_text = font.render(f"raw dt: {dt:.4f} s", True, (220, 220, 230))
        eff_text = font.render(f"effective dt (with time_scale): {effective_dt:.4f} s", True, (220, 220, 230))
        scale_text = font.render(f"time_scale: {time_scale:.2f} (hold SPACE for slow motion)", True, (220, 220, 230))
        fps_text = font.render(f"FPS (approx): {clock.get_fps():.1f}", True, (220, 220, 230))

        screen.blit(dt_text, (20, 20))
        screen.blit(eff_text, (20, 50))
        screen.blit(scale_text, (20, 80))
        screen.blit(fps_text, (20, 110))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

