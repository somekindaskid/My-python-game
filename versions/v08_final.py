"""
Version 8 — Final polish: cube with face, background music, HUD hint.
Equivalent to main.py: full game with FPS-independent physics.
Music: looks for music.mp3 in the project root (parent of versions/).
"""

import pygame
import os
import random

WINDOW_W = 1920
WINDOW_H = 1080
PIPE_SEGMENT_WIDTH = 80
GAP_MIN_HEIGHT = 90
GAP_MAX_HEIGHT = 160
BASE_SCROLL_SPEED = 300
SPEED_INCREASE_PER_POINT = 2.0
MAX_DIFFICULTY_SCORE = 50
CUBE_SIZE = 44
CUBE_SMOOTH_SPEED = 8.0
GOAL_SCORE = 999
HUD_HEIGHT = 48
FPS_TARGET = 165
MUSIC_FILENAME = "music.mp3"


def get_asset_path(filename):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, filename)


def load_music():
    path = get_asset_path(MUSIC_FILENAME)
    if os.path.isfile(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
            return True
        except pygame.error:
            pass
    return False


class PipeSegment:
    __slots__ = ("x", "width", "gap_center_y", "gap_half_height", "scored", "was_in_gap")

    def __init__(self, x, width, gap_center_y, gap_half_height):
        self.x = x
        self.width = width
        self.gap_center_y = gap_center_y
        self.gap_half_height = gap_half_height
        self.scored = False
        self.was_in_gap = False

    def gap_top(self):
        return self.gap_center_y - self.gap_half_height

    def gap_bottom(self):
        return self.gap_center_y + self.gap_half_height

    def move(self, dx):
        self.x += dx

    def collides_with_cube(self, cube_rect):
        seg_left = self.x
        seg_right = self.x + self.width
        if cube_rect.right < seg_left or cube_rect.left > seg_right:
            return False
        gap_top = self.gap_top()
        gap_bottom = self.gap_bottom()
        if cube_rect.bottom < gap_top or cube_rect.top > gap_bottom:
            return True
        return False

    def is_in_gap(self, cube_rect):
        seg_left = self.x
        seg_right = self.x + self.width
        if cube_rect.right < seg_left or cube_rect.left > seg_right:
            return False
        cx = (cube_rect.left + cube_rect.right) / 2
        cy = (cube_rect.top + cube_rect.bottom) / 2
        gap_top = self.gap_top()
        gap_bottom = self.gap_bottom()
        return gap_top <= cy <= gap_bottom

    def is_passed_cube(self, cube_x):
        return self.x + self.width < cube_x


def spawn_segment(x, play_top, play_bottom):
    gap_height = random.uniform(GAP_MIN_HEIGHT, GAP_MAX_HEIGHT)
    half = gap_height / 2
    center_min = play_top + half + 10
    center_max = play_bottom - half - 10
    gap_center_y = random.uniform(center_min, center_max)
    return PipeSegment(x, PIPE_SEGMENT_WIDTH, gap_center_y, half)


def draw_cube_with_face(surface, rect, color=(70, 130, 200)):
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, (40, 80, 140), rect, 2, border_radius=6)
    eye_w, eye_h = 8, 10
    left_eye = pygame.Rect(rect.left + 10, rect.top + 12, eye_w, eye_h)
    right_eye = pygame.Rect(rect.right - 18, rect.top + 12, eye_w, eye_h)
    pygame.draw.ellipse(surface, (255, 255, 255), left_eye)
    pygame.draw.ellipse(surface, (255, 255, 255), right_eye)
    pygame.draw.ellipse(surface, (20, 20, 30), (left_eye.left + 2, left_eye.top + 3, 4, 5))
    pygame.draw.ellipse(surface, (20, 20, 30), (right_eye.left + 2, right_eye.top + 3, 4, 5))
    smile_rect = pygame.Rect(rect.left + 12, rect.top + 26, 20, 10)
    pygame.draw.arc(surface, (30, 30, 40), smile_rect, 0, 3.14159, 2)


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.SCALED)
    pygame.display.set_caption("Cube Jump")
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 42)
    font_hud = pygame.font.Font(None, 36)

    play_top = HUD_HEIGHT
    play_bottom = WINDOW_H
    cube_x = 100.0
    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
    cube_target_y = cube_y
    score = 0
    segments = []
    game_over = False
    won = False
    surprise_shown = False
    load_music()

    running = True
    while running:
        dt_sec = clock.tick(FPS_TARGET) / 1000.0
        if dt_sec <= 0:
            dt_sec = 0.001

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if game_over or won:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_over = False
                    won = False
                    surprise_shown = False
                    score = 0
                    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
                    cube_target_y = cube_y
                    segments.clear()

        if not running:
            break

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cube_target_y = max(play_top, min(play_bottom - CUBE_SIZE, mouse_y - CUBE_SIZE // 2))

        if not game_over and not won:
            effective_difficulty = min(score, MAX_DIFFICULTY_SCORE)
            scroll_speed = BASE_SCROLL_SPEED + effective_difficulty * SPEED_INCREASE_PER_POINT
            move = scroll_speed * dt_sec

            cube_y += (cube_target_y - cube_y) * min(1.0, CUBE_SMOOTH_SPEED * dt_sec)
            cube_rect = pygame.Rect(int(cube_x), int(cube_y), CUBE_SIZE, CUBE_SIZE)

            for seg in segments:
                seg.move(-move)
                if seg.collides_with_cube(cube_rect):
                    game_over = True
                    break
                if seg.is_in_gap(cube_rect):
                    seg.was_in_gap = True
                if not seg.scored and seg.was_in_gap and seg.is_passed_cube(cube_x):
                    seg.scored = True
                    score += 1
                    if score >= GOAL_SCORE:
                        won = True
                        break

            segments = [s for s in segments if s.x + s.width > 0]
            spawn_margin = PIPE_SEGMENT_WIDTH + random.randint(60, 140)
            if not segments or segments[-1].x < WINDOW_W - spawn_margin:
                segments.append(spawn_segment(WINDOW_W, play_top, play_bottom))

        screen.fill((24, 28, 36))
        pygame.draw.line(screen, (60, 60, 70), (0, HUD_HEIGHT), (WINDOW_W, HUD_HEIGHT), 2)
        hud_text = f"Gaps: {score} / {GOAL_SCORE}"
        if not game_over and not won:
            hud_text += "  |  Glide with mouse!"
        screen.blit(font_hud.render(hud_text, True, (220, 220, 230)), (20, 12))

        for seg in segments:
            gap_t = seg.gap_top()
            gap_b = seg.gap_bottom()
            pygame.draw.rect(screen, (50, 55, 75), (seg.x, play_top, seg.width, gap_t - play_top))
            pygame.draw.rect(screen, (50, 55, 75), (seg.x, gap_b, seg.width, play_bottom - gap_b))
            pygame.draw.rect(screen, (70, 78, 100), (seg.x, play_top, seg.width, gap_t - play_top), 1)
            pygame.draw.rect(screen, (70, 78, 100), (seg.x, gap_b, seg.width, play_bottom - gap_b), 1)

        draw_cube_with_face(screen, pygame.Rect(int(cube_x), int(cube_y), CUBE_SIZE, CUBE_SIZE))

        if game_over:
            overlay = pygame.Surface((WINDOW_W, WINDOW_H))
            overlay.set_alpha(200)
            overlay.fill((20, 20, 30))
            screen.blit(overlay, (0, 0))
            msg = font_large.render("Oops! Hit the pipe. Press SPACE to retry.", True, (255, 200, 200))
            screen.blit(msg, msg.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2)))

        if won and not surprise_shown:
            surprise_shown = True
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

        if won:
            overlay = pygame.Surface((WINDOW_W, WINDOW_H))
            overlay.set_alpha(220)
            overlay.fill((25, 35, 50))
            screen.blit(overlay, (0, 0))
            title = font_large.render("SECRET SURPRISE!", True, (255, 215, 100))
            screen.blit(title, title.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 50)))
            sub = font_hud.render("You reached 999 gaps! You're a champion.", True, (200, 220, 255))
            screen.blit(sub, sub.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2)))
            again = font_hud.render("Press SPACE to play again", True, (180, 255, 180))
            screen.blit(again, again.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 + 50)))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
