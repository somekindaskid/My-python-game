import pygame

WINDOW_W, WINDOW_H = 800, 600
FPS_TARGET = 60          # how many times per second we *aim* to draw
SPEED = 200.0            # cube speed in pixels per second


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Delta time example")
    clock = pygame.time.Clock()

    x = 100.0
    y = WINDOW_H / 2 - 25
    running = True

    while running:
        # dt is "delta time": how many seconds passed since the last frame
        dt = clock.tick(FPS_TARGET) / 1000.0
        if dt <= 0:
            dt = 0.001

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move at SPEED pixels per second, regardless of FPS
        x += SPEED * dt

        # Wrap around the screen so you can watch it forever
        if x > WINDOW_W:
            x = -50

        screen.fill((24, 28, 36))
        pygame.draw.rect(screen, (70, 130, 200), (int(x), int(y), 50, 50))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

