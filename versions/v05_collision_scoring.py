"""
Version 5 — Collision, scoring, game over.
Hit wall = game over; pass through gap = +1 point. SPACE to retry.
"""

import pygame
import random

WINDOW_W = 900
WINDOW_H = 600
HUD_HEIGHT = 48
CUBE_SIZE = 44
CUBE_X = 100
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
        "scored": False,
        "was_in_gap": False,
    }


def collides(cube_rect, seg):
    seg_left = seg["x"]
    seg_right = seg["x"] + seg["width"]
    if cube_rect.right < seg_left or cube_rect.left > seg_right:
        return False
    gap_t = seg["gap_center_y"] - seg["gap_half_height"]
    gap_b = seg["gap_center_y"] + seg["gap_half_height"]
    if cube_rect.bottom < gap_t or cube_rect.top > gap_b:
        return True
    return False


def is_in_gap(cube_rect, seg):
    seg_left = seg["x"]
    seg_right = seg["x"] + seg["width"]
    if cube_rect.right < seg_left or cube_rect.left > seg_right:
        return False
    cx = (cube_rect.left + cube_rect.right) / 2
    cy = (cube_rect.top + cube_rect.bottom) / 2
    gap_t = seg["gap_center_y"] - seg["gap_half_height"]
    gap_b = seg["gap_center_y"] + seg["gap_half_height"]
    return gap_t <= cy <= gap_b


def is_passed(cube_x, seg):
    return seg["x"] + seg["width"] < cube_x


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.SCALED)
    pygame.display.set_caption("Cube Jump")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 42)

    play_top = HUD_HEIGHT
    play_bottom = WINDOW_H
    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
    score = 0
    segments = [spawn_segment(WINDOW_W, play_top, play_bottom)]
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_over = False
                score = 0
                cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
                segments = [spawn_segment(WINDOW_W, play_top, play_bottom)]

        if not running:
            break

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cube_target_y = max(play_top, min(play_bottom - CUBE_SIZE, mouse_y - CUBE_SIZE // 2))
        cube_y = cube_target_y
        cube_rect = pygame.Rect(CUBE_X, int(cube_y), CUBE_SIZE, CUBE_SIZE)

        if not game_over:
            for seg in segments:
                seg["x"] -= SCROLL_PX_PER_FRAME
                if collides(cube_rect, seg):
                    game_over = True
                    break
                if is_in_gap(cube_rect, seg):
                    seg["was_in_gap"] = True
                if not seg["scored"] and seg["was_in_gap"] and is_passed(CUBE_X, seg):
                    seg["scored"] = True
                    score += 1

            segments = [s for s in segments if s["x"] + s["width"] > 0]
            if not segments or segments[-1]["x"] < WINDOW_W - PIPE_SEGMENT_WIDTH - 100:
                segments.append(spawn_segment(WINDOW_W, play_top, play_bottom))

        screen.fill((24, 28, 36))
        pygame.draw.line(screen, (60, 60, 70), (0, HUD_HEIGHT), (WINDOW_W, HUD_HEIGHT), 2)
        hud = font.render(f"Gaps: {score}", True, (220, 220, 230))
        screen.blit(hud, (20, 12))

        for seg in segments:
            gap_t = seg["gap_center_y"] - seg["gap_half_height"]
            gap_b = seg["gap_center_y"] + seg["gap_half_height"]
            pygame.draw.rect(screen, (50, 55, 75), (seg["x"], play_top, seg["width"], gap_t - play_top))
            pygame.draw.rect(screen, (50, 55, 75), (seg["x"], gap_b, seg["width"], play_bottom - gap_b))
            pygame.draw.rect(screen, (70, 78, 100), (seg["x"], play_top, seg["width"], gap_t - play_top), 1)
            pygame.draw.rect(screen, (70, 78, 100), (seg["x"], gap_b, seg["width"], play_bottom - gap_b), 1)

        pygame.draw.rect(screen, (70, 130, 200), cube_rect, border_radius=6)
        pygame.draw.rect(screen, (40, 80, 140), cube_rect, 2, border_radius=6)

        if game_over:
            overlay = pygame.Surface((WINDOW_W, WINDOW_H))
            overlay.set_alpha(200)
            overlay.fill((20, 20, 30))
            screen.blit(overlay, (0, 0))
            msg = font.render("Oops! Hit the pipe. Press SPACE to retry.", True, (255, 200, 200))
            r = msg.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2))
            screen.blit(msg, r)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
