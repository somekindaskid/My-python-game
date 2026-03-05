import pygame
import os
import random

# -----------------------------------------------------------------------------
# Constants (all speeds in per-second so physics work at any FPS)
# -----------------------------------------------------------------------------
WINDOW_W = 800
WINDOW_H = 800
PIPE_SEGMENT_WIDTH = 80
GAP_MIN_HEIGHT = 90
GAP_MAX_HEIGHT = 160
BASE_SCROLL_SPEED = 600         # pixels per second
SPEED_INCREASE_PER_POINT = 2.0    # capped by difficulty at score 50
MAX_DIFFICULTY_SCORE = 50
CUBE_SIZE = 44
CUBE_BORDER_RADIUS = 6          # rounded corners; hitbox matches this shape
CUBE_SMOOTH_SPEED = 80          # how fast cube follows mouse (per second)
GOAL_SCORE = 999
HUD_HEIGHT = 48
FPS_TARGET = 165                   # for display only; logic uses delta time
PIPE_GAP_MIN = 200                # medium default; overridden by difficulty
PIPE_GAP_MAX = 320
# Difficulty presets: base_scroll, speed_per_point, gap_min, gap_max, gap_height_min, gap_height_max
DIFFICULTIES = {
    "easy": {"base_scroll": 380, "speed_per_point": 1.0, "pipe_gap_min": 280, "pipe_gap_max": 400, "gap_h_min": 110, "gap_h_max": 190},
    "medium": {"base_scroll": 460, "speed_per_point": 1.2, "pipe_gap_min": 240, "pipe_gap_max": 360, "gap_h_min": 100, "gap_h_max": 170},
    "hard": {"base_scroll": 540, "speed_per_point": 1.6, "pipe_gap_min": 200, "pipe_gap_max": 290, "gap_h_min": 88, "gap_h_max": 150},
}
# Flap mode (Flappy Bird style)
GRAVITY = 780.0                   # pixels per second^2 downward (higher = fall quicker)
FLAP_IMPULSE = -320.0             # upward velocity on flap (pixels per second)
MAX_FALL_SPEED = 580.0            # cap downward speed (higher with gravity for snappier fall)

# Path to your music file - place your MP3 in the game folder and set this name
MUSIC_FILENAME = "music.mp3"
# Home screen beat reaction: interval between beats in ms (e.g. 500 = 120 BPM). Tune to match your song.
HOME_BEAT_INTERVAL_MS = 500
HOME_BEAT_PULSE_SCALE = 0.14   # how much the title scales on each beat (e.g. 0.14 = 14% bigger at hit)
HOME_BEAT_DECAY = 5.0          # how fast the pulse falls off (higher = snappier)

# Time attack mode
TIME_ATTACK_GOAL = 30
TIME_ATTACK_SECONDS = 60.0

# Flappy mode: flap control only; gaps stay in a narrow vertical band (less up/down travel)
FLAPPY_GAP_CENTER_RANGE = 130

# Slow-down: 5 gaps = full charge (2 segments), hold SPACE to slow (3s total when full); cooldown between uses
SLOW_CHARGE_MAX = 2.0
SLOW_CHARGE_PER_GAP = SLOW_CHARGE_MAX / 5.0  # 5 gaps to fill
SLOW_DURATION_SEC = 3.0
SLOW_TIME_SCALE = 0.35
SLOW_COOLDOWN_SEC = 2.0

# Visual themes: bg, pipe_fill, pipe_outline, cube_color, cube_outline, hud_line, hud_text
THEMES = {
    "classic": {"bg": (24, 28, 36), "pipe_fill": (50, 55, 75), "pipe_outline": (70, 78, 100), "cube": (70, 130, 200), "cube_outline": (40, 80, 140), "hud_line": (60, 60, 70), "hud_text": (220, 220, 230)},
    "neon": {"bg": (12, 8, 24), "pipe_fill": (80, 20, 120), "pipe_outline": (200, 80, 255), "cube": (0, 255, 200), "cube_outline": (100, 255, 255), "hud_line": (120, 60, 180), "hud_text": (200, 220, 255)},
    "minimal": {"bg": (250, 250, 252), "pipe_fill": (220, 220, 225), "pipe_outline": (180, 180, 190), "cube": (60, 60, 70), "cube_outline": (40, 40, 50), "hud_line": (200, 200, 210), "hud_text": (80, 80, 90)},
}


def get_asset_path(filename):
    """Return path next to the script so it works when run from any cwd."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def load_music(volume=0.6):
    """Load and start background music if the file exists."""
    path = get_asset_path(MUSIC_FILENAME)
    if os.path.isfile(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            return True
        except pygame.error:
            pass
    return False


def _circle_rect_overlap(cx, cy, radius, rect):
    """True if circle (cx, cy, radius) overlaps rect."""
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    return dx * dx + dy * dy <= radius * radius


def rounded_rect_collides_rect(cube_rect, radius, wall_rect):
    """True if rounded rect (cube_rect with border_radius) overlaps wall_rect."""
    x, y = cube_rect.left, cube_rect.top
    w, h = cube_rect.width, cube_rect.height
    r = radius
    if r <= 0 or r * 2 >= min(w, h):
        return cube_rect.colliderect(wall_rect)
    center_rect = pygame.Rect(x + r, y + r, w - 2 * r, h - 2 * r)
    if center_rect.colliderect(wall_rect):
        return True
    corners = [(x + r, y + r), (x + w - r, y + r), (x + r, y + h - r), (x + w - r, y + h - r)]
    for (cx, cy) in corners:
        if _circle_rect_overlap(cx, cy, r, wall_rect):
            return True
    return False


class PipeSegment:
    """One segment of pipe: a vertical strip with a gap at gap_y, gap_height."""

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

    def collides_with_cube(self, cube_rect, play_top, play_bottom, radius=0):
        """True if cube (rounded rect with given radius) overlaps this segment's wall."""
        gap_top = self.gap_top()
        gap_bottom = self.gap_bottom()
        top_wall = pygame.Rect(self.x, play_top, self.width, gap_top - play_top)
        bottom_wall = pygame.Rect(self.x, gap_bottom, self.width, play_bottom - gap_bottom)
        if radius <= 0:
            if cube_rect.colliderect(top_wall) or cube_rect.colliderect(bottom_wall):
                return True
            return False
        if rounded_rect_collides_rect(cube_rect, radius, top_wall):
            return True
        if rounded_rect_collides_rect(cube_rect, radius, bottom_wall):
            return True
        return False

    def is_in_gap(self, cube_rect):
        """True if cube center is inside the gap when overlapping this segment."""
        seg_left = self.x
        seg_right = self.x + self.width
        if cube_rect.right < seg_left or cube_rect.left > seg_right:
            return False
        cx = (cube_rect.left + cube_rect.right) / 2
        cy = (cube_rect.top + cube_rect.bottom) / 2
        if cx < seg_left or cx > seg_right:
            return False
        gap_top = self.gap_top()
        gap_bottom = self.gap_bottom()
        return gap_top <= cy <= gap_bottom

    def is_passed_cube(self, cube_x):
        """True if segment has passed the cube (for giving score once)."""
        return self.x + self.width < cube_x


def spawn_segment(x, play_top, play_bottom, gap_h_min=None, gap_h_max=None, flappy=False):
    """Create a new pipe segment with a random gap. If flappy=True, gap center stays in a narrow vertical band."""
    if gap_h_min is None:
        gap_h_min = GAP_MIN_HEIGHT
    if gap_h_max is None:
        gap_h_max = GAP_MAX_HEIGHT
    gap_height = random.uniform(gap_h_min, gap_h_max)
    half = gap_height / 2
    full_center_min = play_top + half + 10
    full_center_max = play_bottom - half - 10
    if flappy:
        play_center = (play_top + play_bottom) / 2
        center_min = max(full_center_min, play_center - FLAPPY_GAP_CENTER_RANGE)
        center_max = min(full_center_max, play_center + FLAPPY_GAP_CENTER_RANGE)
    else:
        center_min, center_max = full_center_min, full_center_max
    gap_center_y = random.uniform(center_min, center_max)
    return PipeSegment(x, PIPE_SEGMENT_WIDTH, gap_center_y, half)


def draw_cube_with_face(surface, rect, theme_dict, ghost_alpha=None):
    """Draw a rounded cube with eyes and a smile. theme_dict has 'cube' and 'cube_outline'. If ghost_alpha set, draw semi-transparent."""
    color = theme_dict["cube"]
    outline = theme_dict["cube_outline"]
    if ghost_alpha is not None:
        s = pygame.Surface((rect.w + 4, rect.h + 4))
        s.set_alpha(ghost_alpha)
        s.fill((0, 0, 0))
        s.set_colorkey((0, 0, 0))
        r2 = pygame.Rect(2, 2, rect.w, rect.h)
        pygame.draw.rect(s, color, r2, border_radius=6)
        pygame.draw.rect(s, outline, r2, 2, border_radius=6)
        surface.blit(s, (rect.x - 2, rect.y - 2))
        return
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, outline, rect, 2, border_radius=6)
    eye_w, eye_h = 8, 10
    left_eye = pygame.Rect(rect.left + 10, rect.top + 12, eye_w, eye_h)
    right_eye = pygame.Rect(rect.right - 18, rect.top + 12, eye_w, eye_h)
    pygame.draw.ellipse(surface, (255, 255, 255), left_eye)
    pygame.draw.ellipse(surface, (255, 255, 255), right_eye)
    pygame.draw.ellipse(surface, (20, 20, 30), (left_eye.left + 2, left_eye.top + 3, 4, 5))
    pygame.draw.ellipse(surface, (20, 20, 30), (right_eye.left + 2, right_eye.top + 3, 4, 5))
    smile_rect = pygame.Rect(rect.left + 12, rect.top + 26, 20, 10)
    pygame.draw.arc(surface, (30, 30, 40), smile_rect, 0, 3.14159, 2)


def run_game():
    pygame.init()
    pygame.mixer.init()
    fullscreen = False
    win_w, win_h = WINDOW_W, WINDOW_H
    screen = pygame.display.set_mode((win_w, win_h), pygame.SCALED)
    pygame.display.set_caption("Cube Jump")
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 42)
    font_hud = pygame.font.Font(None, 36)

    play_top = HUD_HEIGHT
    play_bottom = win_h
    cube_x = 100.0
    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
    cube_target_y = cube_y
    score = 0
    scroll_speed = BASE_SCROLL_SPEED
    segments = []
    game_over = False
    won = False
    surprise_shown = False
    on_play_screen = True
    mod_menu_open = False
    show_hitbox = False
    control_mode = "mouse"
    cube_velocity_y = 0.0
    cursor_visible = True
    difficulty = "medium"
    game_mode = "normal"  # "normal", "time_attack", or "flappy"
    time_attack_remaining = TIME_ATTACK_SECONDS
    elapsed_time = 0.0
    theme = "classic"
    music_volume = 0.6
    sfx_volume = 0.8
    ghost_data = []
    current_run_recording = []
    show_ghost = False
    slow_charge = 0.0
    slow_cooldown_remaining = 0.0
    slow_was_active_prev = False
    load_music(music_volume)

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                cursor_visible = not cursor_visible
                pygame.mouse.set_visible(cursor_visible)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    win_w, win_h = screen.get_size()
                else:
                    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.SCALED)
                    win_w, win_h = WINDOW_W, WINDOW_H
                play_bottom = win_h
            if on_play_screen:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    on_play_screen = False
                    current_run_recording = []
                    slow_charge = 0.0
                    slow_cooldown_remaining = 0.0
                    slow_was_active_prev = False
                    if game_mode == "flappy":
                        control_mode = "flap"
                    if game_mode == "time_attack":
                        time_attack_remaining = TIME_ATTACK_SECONDS
                    elapsed_time = 0.0
                    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
                    cube_target_y = cube_y
                    cube_velocity_y = 0.0
                    segments.clear()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_KP1):
                    difficulty = "easy"
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_2, pygame.K_KP2):
                    difficulty = "medium"
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_3, pygame.K_KP3):
                    difficulty = "hard"
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_4, pygame.K_KP4):
                    game_mode = "normal"
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_5, pygame.K_KP5):
                    game_mode = "time_attack"
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_6, pygame.K_KP6):
                    game_mode = "flappy"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    theme = {"classic": "neon", "neon": "minimal", "minimal": "classic"}[theme]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    on_play_screen = False
                    current_run_recording = []
                    slow_charge = 0.0
                    slow_cooldown_remaining = 0.0
                    slow_was_active_prev = False
                    if game_mode == "flappy":
                        control_mode = "flap"
                    if game_mode == "time_attack":
                        time_attack_remaining = TIME_ATTACK_SECONDS
                    elapsed_time = 0.0
                    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
                    cube_target_y = cube_y
                    cube_velocity_y = 0.0
                    segments.clear()
            if game_over or won:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_over = False
                    won = False
                    surprise_shown = False
                    score = 0
                    scroll_speed = BASE_SCROLL_SPEED
                    cube_y = (play_top + play_bottom) / 2 - CUBE_SIZE / 2
                    cube_target_y = cube_y
                    cube_velocity_y = 0.0
                    segments.clear()
                    current_run_recording = []
                    elapsed_time = 0.0
                    slow_charge = 0.0
                    slow_cooldown_remaining = 0.0
                    slow_was_active_prev = False
                    if game_mode == "time_attack":
                        time_attack_remaining = TIME_ATTACK_SECONDS
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                if not on_play_screen and not game_over and not won:
                    mod_menu_open = not mod_menu_open
            if mod_menu_open:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        show_hitbox = not show_hitbox
                    if event.key == pygame.K_c:
                        control_mode = "flap" if control_mode == "mouse" else "mouse"
                        if control_mode == "mouse":
                            cube_velocity_y = 0.0
                    if event.key == pygame.K_g:
                        theme = {"classic": "neon", "neon": "minimal", "minimal": "classic"}[theme]
                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            win_w, win_h = screen.get_size()
                        else:
                            screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.SCALED)
                            win_w, win_h = WINDOW_W, WINDOW_H
                        play_bottom = win_h
                    if event.key == pygame.K_r:
                        show_ghost = not show_ghost
                    if event.key == pygame.K_q:
                        music_volume = min(1.0, music_volume + 0.1)
                        pygame.mixer.music.set_volume(music_volume)
                    if event.key == pygame.K_a:
                        music_volume = max(0.0, music_volume - 0.1)
                        pygame.mixer.music.set_volume(music_volume)
                    if event.key == pygame.K_z:
                        sfx_volume = min(1.0, sfx_volume + 0.1)
                    if event.key == pygame.K_x:
                        sfx_volume = max(0.0, sfx_volume - 0.1)
            elif not on_play_screen and not game_over and not won and control_mode == "flap":
                if event.type == pygame.KEYDOWN and event.key not in (pygame.K_ESCAPE, pygame.K_TAB):
                    cube_velocity_y = FLAP_IMPULSE

        if not running:
            break

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cube_target_y = max(play_top, min(play_bottom - CUBE_SIZE, mouse_y - CUBE_SIZE // 2))

        if on_play_screen:
            th = THEMES[theme]
            screen.fill(th["bg"])
            # Beat reaction: drive pulse from music position (or time if no music)
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms < 0:
                pos_ms = pygame.time.get_ticks()
            phase = (pos_ms % HOME_BEAT_INTERVAL_MS) / max(1, HOME_BEAT_INTERVAL_MS)
            pulse = max(0.0, 1.0 - phase) ** HOME_BEAT_DECAY
            scale = 1.0 + HOME_BEAT_PULSE_SCALE * pulse

            font_title = pygame.font.Font(None, 72)
            title = font_title.render("Cube Jump", True, (255, 215, 100))
            tw, th = title.get_size()
            scaled_w = max(1, int(tw * scale))
            scaled_h = max(1, int(th * scale))
            title_scaled = pygame.transform.smoothscale(title, (scaled_w, scaled_h))
            tr = title_scaled.get_rect(center=(win_w // 2, win_h // 2 - 60))
            screen.blit(title_scaled, tr)
            sub = font_large.render("Glide through the pipe with your mouse", True, (200, 220, 255))
            sr = sub.get_rect(center=(win_w // 2, win_h // 2))
            screen.blit(sub, sr)
            diff_names = ("Easy", "Medium", "Hard")
            diff_colors = ((150, 255, 150), (255, 215, 100), (255, 150, 150))
            diff_y = win_h // 2 + 30
            for i, name in enumerate(diff_names):
                is_sel = (difficulty == name.lower())
                color = diff_colors[i] if is_sel else (140, 140, 150)
                t = font_hud.render(name, True, color)
                x = win_w // 2 + (i - 1) * 140
                screen.blit(t, t.get_rect(center=(x, diff_y)))
            mode_txt = "4=Normal  5=Time attack  6=Flappy (flap, narrow gaps)"
            mode_surf = font_hud.render(mode_txt, True, (180, 220, 255))
            screen.blit(mode_surf, mode_surf.get_rect(center=(win_w // 2, win_h // 2 + 78)))
            theme_txt = f"G = theme: {theme.capitalize()}"
            theme_surf = font_hud.render(theme_txt, True, (160, 200, 220))
            screen.blit(theme_surf, theme_surf.get_rect(center=(win_w // 2, win_h // 2 + 98)))
            start = font_hud.render("1 2 3 = difficulty  |  SPACE or click to play", True, (180, 255, 180))
            start_r = start.get_rect(center=(win_w // 2, win_h // 2 + 58))
            screen.blit(start, start_r)
            pygame.display.flip()
            continue

        if not mod_menu_open and not game_over and not won:
            elapsed_time += dt_sec
            current_run_recording.append((elapsed_time, cube_y))
            if game_mode == "time_attack":
                time_attack_remaining -= dt_sec
                if time_attack_remaining <= 0:
                    game_over = True
                    ghost_data = list(current_run_recording)
            diff_params = DIFFICULTIES[difficulty]
            effective = min(score, MAX_DIFFICULTY_SCORE)
            scroll_speed = diff_params["base_scroll"] + effective * diff_params["speed_per_point"]

            # Slow-down: hold SPACE to slow (drains charge); cooldown after each use
            slow_cooldown_remaining = max(0.0, slow_cooldown_remaining - dt_sec)
            can_use_slow = slow_cooldown_remaining <= 0
            space_held = pygame.key.get_pressed()[pygame.K_SPACE]
            if space_held and slow_charge > 0 and can_use_slow:
                time_scale = SLOW_TIME_SCALE
                drain = (SLOW_CHARGE_MAX / SLOW_DURATION_SEC) * dt_sec
                slow_charge = max(0.0, slow_charge - drain)
                used_slow_this_frame = True
            else:
                time_scale = 1.0
                used_slow_this_frame = False
            if slow_was_active_prev and not used_slow_this_frame:
                slow_cooldown_remaining = SLOW_COOLDOWN_SEC
            slow_was_active_prev = used_slow_this_frame
            effective_dt = dt_sec * time_scale

            move = scroll_speed * effective_dt

            if control_mode == "mouse":
                cube_y += (cube_target_y - cube_y) * min(1.0, CUBE_SMOOTH_SPEED * effective_dt)
            else:
                cube_velocity_y += GRAVITY * effective_dt
                if cube_velocity_y > MAX_FALL_SPEED:
                    cube_velocity_y = MAX_FALL_SPEED
                cube_y += cube_velocity_y * effective_dt
                cube_y = max(play_top, min(play_bottom - CUBE_SIZE, cube_y))
                if cube_y <= play_top or cube_y >= play_bottom - CUBE_SIZE:
                    cube_velocity_y = 0.0

            cube_rect = pygame.Rect(int(cube_x), int(cube_y), CUBE_SIZE, CUBE_SIZE)

            for seg in segments:
                seg.move(-move)
                if seg.collides_with_cube(cube_rect, play_top, play_bottom, CUBE_BORDER_RADIUS):
                    game_over = True
                    ghost_data = list(current_run_recording)
                    break
                if seg.is_in_gap(cube_rect):
                    seg.was_in_gap = True
                if not seg.scored and seg.was_in_gap and seg.is_passed_cube(cube_x):
                    seg.scored = True
                    score += 1
                    slow_charge = min(SLOW_CHARGE_MAX, slow_charge + SLOW_CHARGE_PER_GAP)
                    goal = TIME_ATTACK_GOAL if game_mode == "time_attack" else GOAL_SCORE
                    if score >= goal:
                        won = True
                        ghost_data = list(current_run_recording)
                        break

            segments = [s for s in segments if s.x + s.width > 0]
            gap_between = random.randint(diff_params["pipe_gap_min"], diff_params["pipe_gap_max"])
            spawn_margin = PIPE_SEGMENT_WIDTH + gap_between
            if not segments or segments[-1].x < win_w - spawn_margin:
                seg = spawn_segment(
                    win_w, play_top, play_bottom,
                    diff_params["gap_h_min"], diff_params["gap_h_max"],
                    flappy=(game_mode == "flappy"),
                )
                segments.append(seg)

        th = THEMES[theme]
        screen.fill(th["bg"])
        pygame.draw.line(screen, th["hud_line"], (0, HUD_HEIGHT), (win_w, HUD_HEIGHT), 2)

        goal = TIME_ATTACK_GOAL if game_mode == "time_attack" else GOAL_SCORE
        hud_text = f"Gaps: {score} / {goal}  |  {difficulty.capitalize()}"
        if game_mode == "time_attack":
            hud_text += f"  |  Time: {max(0, int(time_attack_remaining))}s"
        if game_mode == "flappy":
            hud_text += "  |  Flappy"
        if not game_over and not won:
            if control_mode == "mouse":
                hud_text += "  |  Glide with mouse!"
            else:
                hud_text += "  |  Flap: any key (TAB = mods)"
        hud_text += "  |  TAB = Mod menu"
        text_surf = font_hud.render(hud_text, True, th["hud_text"])
        screen.blit(text_surf, (20, 12))
        # Slow meter: 2 segments = full, hold SPACE to use; cooldown between uses
        if not on_play_screen:
            meter_x, meter_y = win_w - 100, 14
            slow_label = font_hud.render("Slow", True, th["hud_text"])
            screen.blit(slow_label, (meter_x - 36, meter_y - 2))
            seg_w, seg_h = 22, 10
            on_cooldown = slow_cooldown_remaining > 0
            for i in range(2):
                rx = meter_x + i * (seg_w + 2)
                if on_cooldown:
                    fill = (60, 60, 70)
                else:
                    fill = (100, 200, 255) if slow_charge > i else (50, 50, 60)
                pygame.draw.rect(screen, fill, (rx, meter_y, seg_w, seg_h))
                pygame.draw.rect(screen, th["hud_line"], (rx, meter_y, seg_w, seg_h), 1)
            hint = f"Hold SPACE  |  {max(0, int(slow_cooldown_remaining))}s CD" if on_cooldown else "Hold SPACE"
            hint_slow = font_hud.render(hint, True, (150, 180, 220))
            screen.blit(hint_slow, (meter_x - 24, meter_y + 14))

        for seg in segments:
            gap_t = seg.gap_top()
            gap_b = seg.gap_bottom()
            pygame.draw.rect(screen, th["pipe_fill"], (seg.x, play_top, seg.width, gap_t - play_top))
            pygame.draw.rect(screen, th["pipe_fill"], (seg.x, gap_b, seg.width, play_bottom - gap_b))
            pygame.draw.rect(screen, th["pipe_outline"], (seg.x, play_top, seg.width, gap_t - play_top), 1)
            pygame.draw.rect(screen, th["pipe_outline"], (seg.x, gap_b, seg.width, play_bottom - gap_b), 1)

        if show_ghost and ghost_data and not on_play_screen:
            ghost_y = None
            for i in range(len(ghost_data) - 1):
                t0, y0 = ghost_data[i]
                t1, y1 = ghost_data[i + 1]
                if t0 <= elapsed_time <= t1:
                    if t1 > t0:
                        f = (elapsed_time - t0) / (t1 - t0)
                        ghost_y = y0 + f * (y1 - y0)
                    else:
                        ghost_y = y0
                    break
            if ghost_y is None and ghost_data and elapsed_time >= ghost_data[-1][0]:
                ghost_y = ghost_data[-1][1]
            elif ghost_y is None and ghost_data and elapsed_time <= ghost_data[0][0]:
                ghost_y = ghost_data[0][1]
            if ghost_y is not None:
                ghost_rect = pygame.Rect(int(cube_x), int(ghost_y), CUBE_SIZE, CUBE_SIZE)
                draw_cube_with_face(screen, ghost_rect, th, ghost_alpha=100)
        draw_cube_with_face(screen, pygame.Rect(int(cube_x), int(cube_y), CUBE_SIZE, CUBE_SIZE), th)
        if show_hitbox:
            hitbox_rect = pygame.Rect(int(cube_x), int(cube_y), CUBE_SIZE, CUBE_SIZE)
            pygame.draw.rect(screen, (0, 255, 100), hitbox_rect, 2, border_radius=CUBE_BORDER_RADIUS)

        if mod_menu_open:
            overlay = pygame.Surface((win_w, win_h))
            overlay.set_alpha(220)
            overlay.fill((20, 25, 35))
            screen.blit(overlay, (0, 0))
            font_mod = pygame.font.Font(None, 48)
            title = font_mod.render("Mod Menu  (TAB to close)", True, (255, 215, 100))
            tr = title.get_rect(center=(win_w // 2, win_h // 2 - 140))
            screen.blit(title, tr)
            y_off = -100
            hb = font_mod.render(f"Show hitbox: {'ON' if show_hitbox else 'OFF'}  (H)", True, (220, 220, 230))
            screen.blit(hb, hb.get_rect(center=(win_w // 2, win_h // 2 + y_off)))
            y_off += 28
            ctrl = font_mod.render(f"Control: {control_mode.capitalize()}  (C)", True, (220, 220, 230))
            screen.blit(ctrl, ctrl.get_rect(center=(win_w // 2, win_h // 2 + y_off)))
            y_off += 28
            gtr = font_mod.render(f"Theme: {theme.capitalize()}  (G)", True, (220, 220, 230))
            screen.blit(gtr, gtr.get_rect(center=(win_w // 2, win_h // 2 + y_off)))
            y_off += 28
            ftr = font_mod.render(f"Fullscreen: {'ON' if fullscreen else 'OFF'}  (F)", True, (220, 220, 230))
            screen.blit(ftr, ftr.get_rect(center=(win_w // 2, win_h // 2 + y_off)))
            y_off += 28
            ghr = font_mod.render(f"Ghost replay: {'ON' if show_ghost else 'OFF'}  (R)", True, (220, 220, 230))
            screen.blit(ghr, ghr.get_rect(center=(win_w // 2, win_h // 2 + y_off)))
            y_off += 28
            music_pct = int(music_volume * 100)
            mtr = font_mod.render(f"Music: {music_pct}%  (Q/A)", True, (220, 220, 230))
            screen.blit(mtr, mtr.get_rect(center=(win_w // 2, win_h // 2 + y_off)))
            y_off += 28
            sfx_pct = int(sfx_volume * 100)
            str_ = font_mod.render(f"SFX: {sfx_pct}%  (Z/X)", True, (220, 220, 230))
            screen.blit(str_, str_.get_rect(center=(win_w // 2, win_h // 2 + y_off)))
            y_off += 36
            hint = font_hud.render("Mouse/Flap  |  F11 = fullscreen anywhere", True, (180, 200, 220))
            screen.blit(hint, hint.get_rect(center=(win_w // 2, win_h // 2 + y_off)))

        if game_over:
            overlay = pygame.Surface((win_w, win_h))
            overlay.set_alpha(200)
            overlay.fill((20, 20, 30))
            screen.blit(overlay, (0, 0))
            msg_txt = "Time's up! Press SPACE to retry." if game_mode == "time_attack" and time_attack_remaining <= 0 else "Oops! Hit the pipe. Press SPACE to retry."
            msg = font_large.render(msg_txt, True, (255, 200, 200))
            r = msg.get_rect(center=(win_w // 2, win_h // 2))
            screen.blit(msg, r)

        if won and not surprise_shown:
            surprise_shown = True
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

        if won:
            overlay = pygame.Surface((win_w, win_h))
            overlay.set_alpha(220)
            overlay.fill((25, 35, 50))
            screen.blit(overlay, (0, 0))
            if game_mode == "time_attack":
                title = font_large.render("Time attack complete!", True, (255, 215, 100))
                sub_txt = f"You got 30 gaps in {int(elapsed_time)} seconds!"
            else:
                title = font_large.render("SECRET SURPRISE!", True, (255, 215, 100))
                sub_txt = "You reached 999 gaps! You're a champion." if game_mode != "flappy" else "You reached 999 gaps! Flappy champion."
            tr = title.get_rect(center=(win_w // 2, win_h // 2 - 50))
            screen.blit(title, tr)
            sub = font_hud.render(sub_txt, True, (200, 220, 255))
            sr = sub.get_rect(center=(win_w // 2, win_h // 2))
            screen.blit(sub, sr)
            again = font_hud.render("Press SPACE to play again", True, (180, 255, 180))
            ar = again.get_rect(center=(win_w // 2, win_h // 2 + 50))
            screen.blit(again, ar)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_game()
