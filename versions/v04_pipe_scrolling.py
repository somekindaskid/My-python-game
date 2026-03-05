"""
Version 4 — Pipe and gaps (scrolling).
Pipe segments with random gaps scroll left; no collision yet.
"""

import pygame
import random

WINDOW_W = 900
WINDOW_H = 600
HUD_HEIGHT = 48
CUBE_SIZE = 44
PIPE_SEGMENT_WIDTH = 80
GAP_MIN_HEIGHT = 90
GAP_MAX_HEIGHT = 160
SCROLL_PX_PER_FRAME = 4


def spawn_segment(x, play_top, play_bottom):
    gap_height = random.uniform(GAP_MIN_HEIGHT, GAP_MAX_HEIGHT)
    half = gap_height / 2
    center_min = play_top + half + 10
    center_max = play_bottom - half - 10
    gap_center_y = random.uniform(center_min, center_max)
    return {
        "x": x,
        "width": PIPE_SEGMENT_WIDTH,
        "gap_center_y": gap_center_y,
        "gap_half_height": half,
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.SCALED)
    pygame.display.set_caption("Cube Jump")
    clock = pygame.time.Clock()

    play_top = HUD_HEIGHT
    play_bottom = WINDOW_H
    cube_x = 100
    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
    segments = [spawn_segment(WINDOW_W, play_top, play_bottom)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cube_target_y = mouse_y - CUBE_SIZE // 2
        cube_y = max(play_top, min(play_bottom - CUBE_SIZE, cube_target_y))

        for seg in segments:
            seg["x"] -= SCROLL_PX_PER_FRAME
        segments = [s for s in segments if s["x"] + s["width"] > 0]
        if not segments or segments[-1]["x"] < WINDOW_W - PIPE_SEGMENT_WIDTH - 100:
            segments.append(spawn_segment(WINDOW_W, play_top, play_bottom))

        screen.fill((24, 28, 36))
        pygame.draw.line(screen, (60, 60, 70), (0, HUD_HEIGHT), (WINDOW_W, HUD_HEIGHT), 2)

        for seg in segments:
            gap_t = seg["gap_center_y"] - seg["gap_half_height"]
            gap_b = seg["gap_center_y"] + seg["gap_half_height"]
            pygame.draw.rect(screen, (50, 55, 75), (seg["x"], play_top, seg["width"], gap_t - play_top))
            pygame.draw.rect(screen, (50, 55, 75), (seg["x"], gap_b, seg["width"], play_bottom - gap_b))
            pygame.draw.rect(screen, (70, 78, 100), (seg["x"], play_top, seg["width"], gap_t - play_top), 1)
            pygame.draw.rect(screen, (70, 78, 100), (seg["x"], gap_b, seg["width"], play_bottom - gap_b), 1)

        cube_rect = pygame.Rect(cube_x, int(cube_y), CUBE_SIZE, CUBE_SIZE)
        pygame.draw.rect(screen, (70, 130, 200), cube_rect, border_radius=6)
        pygame.draw.rect(screen, (40, 80, 140), cube_rect, 2, border_radius=6)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
