"""
Version 2 — Drawing the cube.
Static cube drawn on screen; no input yet.
"""

import pygame

WINDOW_W = 900
WINDOW_H = 600
HUD_HEIGHT = 48
CUBE_SIZE = 44


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.SCALED)
    pygame.display.set_caption("Cube Jump")
    clock = pygame.time.Clock()

    play_top = HUD_HEIGHT
    play_bottom = WINDOW_H
    cube_x = 100
    cube_y = (play_top + play_bottom) // 2 - CUBE_SIZE // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill((24, 28, 36))
        pygame.draw.line(screen, (60, 60, 70), (0, HUD_HEIGHT), (WINDOW_W, HUD_HEIGHT), 2)

        cube_rect = pygame.Rect(cube_x, cube_y, CUBE_SIZE, CUBE_SIZE)
        pygame.draw.rect(screen, (70, 130, 200), cube_rect, border_radius=6)
        pygame.draw.rect(screen, (40, 80, 140), cube_rect, 2, border_radius=6)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
