import pygame

from src.ball import Ball
from src.constants import (
    BLACK,
    FPS,
    GOAL_CAPTION_DURATION,
    GOAL_CAPTION_FADE_DURATION,
    GOAL_CAPTION_TEXT,
    GOAL_HEIGHT,
    GOAL_POST_THICKNESS,
    GOAL_WIDTH,
    GOAL_Y,
    GOLD,
    GRAY,
    GREEN,
    GROUND_Y,
    HEIGHT,
    MATCH_WIN_SCORE,
    P1_CONTROLS,
    P2_CONTROLS,
    PLAYER1_IMAGE_PATH,
    PLAYER2_IMAGE_PATH,
    SCORE_TEXT_POS,
    SKY_BLUE,
    WHITE,
    WIDTH,
)
from src.player import Player
from src import display_scaler

_PAUSE_OPTIONS = ["계속하기", "메인 메뉴", "게임 종료"]
_GEAR_RECT = pygame.Rect(WIDTH // 2 - 15, 2, 30, 18)


def draw_goal_caption(screen, font, started_at):
    elapsed = pygame.time.get_ticks() - started_at
    if elapsed >= GOAL_CAPTION_DURATION:
        return False
    remaining = GOAL_CAPTION_DURATION - elapsed
    fade_time = min(elapsed, remaining, GOAL_CAPTION_FADE_DURATION)
    alpha = int(255 * fade_time / GOAL_CAPTION_FADE_DURATION)

    shadow = font.render(GOAL_CAPTION_TEXT, True, BLACK)
    caption = font.render(GOAL_CAPTION_TEXT, True, GOLD)
    shadow.set_alpha(alpha)
    caption.set_alpha(alpha)

    caption_rect = caption.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    screen.blit(shadow, shadow.get_rect(center=(caption_rect.centerx + 6, caption_rect.centery + 6)))
    screen.blit(caption, caption_rect)
    return True


def draw_outlined_text(surface, text, font, color, outline_color, pos, center=False):
    ox, oy = pos
    outline = font.render(text, True, outline_color)
    main = font.render(text, True, color)
    if center:
        ox -= main.get_width() // 2
        oy -= main.get_height() // 2
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)):
        surface.blit(outline, (ox + dx, oy + dy))
    surface.blit(main, (ox, oy))


def draw_gear_button(screen, font):
    pygame.draw.rect(screen, (20, 20, 20), _GEAR_RECT, border_radius=4)
    pygame.draw.rect(screen, (120, 120, 120), _GEAR_RECT, 1, border_radius=4)
    label = font.render("⚙", True, (200, 200, 200))
    screen.blit(label, label.get_rect(center=_GEAR_RECT.center))


def run_pause_menu(screen, clock, background_snapshot):
    title_font  = pygame.font.SysFont("malgungothic", 26, bold=True)
    option_font = pygame.font.SysFont("malgungothic", 22)
    hint_font   = pygame.font.SysFont("malgungothic", 16)
    selected = 0

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))

    panel_w, panel_h = 260, 200
    panel = pygame.Rect(WIDTH // 2 - panel_w // 2, HEIGHT // 2 - panel_h // 2, panel_w, panel_h)

    while True:
        clock.tick(FPS)
        screen.blit(background_snapshot, (0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (18, 18, 18), panel, border_radius=12)
        pygame.draw.rect(screen, GOLD, panel, 2, border_radius=12)

        title = title_font.render("⚙  일시정지", True, GOLD)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.y + 28)))

        pygame.draw.line(screen, (60, 60, 60), (panel.x + 20, panel.y + 48), (panel.right - 20, panel.y + 48), 1)

        for i, label in enumerate(_PAUSE_OPTIONS):
            cy = panel.y + 72 + i * 38
            if i == selected:
                highlight = pygame.Rect(panel.x + 10, cy - 14, panel_w - 20, 30)
                pygame.draw.rect(screen, (40, 40, 40), highlight, border_radius=6)
                color = GOLD
            else:
                color = WHITE
            text = option_font.render(label, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, cy)))

        hint = hint_font.render("↑↓ 이동   ENTER 확인   ESC 계속", True, GRAY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, panel.bottom - 14)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    display_scaler.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(_PAUSE_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(_PAUSE_OPTIONS)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return ["resume", "title", "quit"][selected]
                elif event.key == pygame.K_ESCAPE:
                    return "resume"


def load_stadium_background(background):
    if not background:
        return None
    try:
        image = pygame.image.load(background["path"]).convert()
    except (pygame.error, FileNotFoundError):
        return None
    return pygame.transform.scale(image, (WIDTH, HEIGHT))


def draw_match_background(screen, background_image):
    if background_image:
        screen.blit(background_image, (0, 0))
        return
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))


def run_match(screen, clock, p1_team, p2_team, stadium_background=None, win_score=MATCH_WIN_SCORE, use_timer=True):
    font       = pygame.font.SysFont("malgungothic", 40, bold=True)
    name_font  = pygame.font.SysFont("malgungothic", 22, bold=True)
    gear_font  = pygame.font.SysFont("malgungothic", 14)
    goal_caption_font = pygame.font.SysFont("malgungothic", 200, bold=True)

    total_time = 90
    start_ticks = pygame.time.get_ticks()
    game_over = False
    game_over_at = None
    is_golden_ball = False
    remaining_time = total_time

    score1, score2 = 0, 0
    goal_caption_started_at = None

    
    p1 = Player(150, 500, P1_CONTROLS, p1_team["color"], PLAYER1_IMAGE_PATH, char_type=p1_team["id"])
    p2 = Player(800, 500, P2_CONTROLS, p2_team["color"], PLAYER2_IMAGE_PATH, char_type=p2_team["id"])
    p1.team_name = p1_team["name"]
    p2.team_name = p2_team["name"]
    ball = Ball()
    background_image = load_stadium_background(stadium_background)

    goal_left  = pygame.Rect(0, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
    goal_right = pygame.Rect(WIDTH - GOAL_WIDTH, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)

    while True:
        clock.tick(FPS)

        if use_timer and not game_over and not is_golden_ball:
            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            remaining_time = max(0, total_time - seconds_passed)
            if remaining_time <= 0:
                if score1 == score2:
                    is_golden_ball = True
                else:
                    game_over = True
                    game_over_at = pygame.time.get_ticks()

        if game_over and game_over_at is not None:
            if pygame.time.get_ticks() - game_over_at > 1500:
                if score1 > score2:
                    return {"winner": p1_team, "loser": p2_team, "score": (score1, score2)}
                else:
                    return {"winner": p2_team, "loser": p1_team, "score": (score1, score2)}

        draw_match_background(screen, background_image)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    display_scaler.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    snapshot = screen.copy()
                    result = run_pause_menu(screen, clock, snapshot)
                    if result in ("title", "quit"):
                        return result
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if _GEAR_RECT.collidepoint(display_scaler.scale_mouse(event.pos)):
                    snapshot = screen.copy()
                    result = run_pause_menu(screen, clock, snapshot)
                    if result in ("title", "quit"):
                        return result

        if not game_over:
            p1.move()
            p2.move()
            ball.update()

        if use_timer and is_golden_ball and score1 != score2:
            game_over = True
            game_over_at = game_over_at or pygame.time.get_ticks()

        br = ball.radius
        if ball.pos[0] - br < GOAL_WIDTH and abs(ball.pos[1] - GOAL_Y) < br:
            ball.vel[1] *= -0.7
            ball.pos[1] = GOAL_Y - br if ball.vel[1] < 0 else GOAL_Y + br
        if ball.pos[0] + br > WIDTH - GOAL_WIDTH and abs(ball.pos[1] - GOAL_Y) < br:
            ball.vel[1] *= -0.7
            ball.pos[1] = GOAL_Y - br if ball.vel[1] < 0 else GOAL_Y + br

        for player in (p1, p2):
            dx = ball.pos[0] - player.circle_x
            dy = ball.pos[1] - player.circle_y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if 0 < dist < player.radius + ball.radius:
                nx = dx / dist
                ny = dy / dist
                pv_n = player.vel_x * nx + player.vel_y * ny
                
                
                kick = (pv_n * player.power) + (5 * player.power)
                
                ball.vel[0] = nx * kick
                ball.vel[1] = ny * kick - 5
                overlap = player.radius + ball.radius - dist
                ball.pos[0] += nx * (overlap + 1)
                ball.pos[1] += ny * (overlap + 1)

        if goal_left.collidepoint(ball.pos[0], ball.pos[1]):
            score2 += 1
            goal_caption_started_at = pygame.time.get_ticks()
            if score2 >= win_score:
                return {"winner": p2_team, "loser": p1_team, "score": (score1, score2)}
            ball.reset()
        if goal_right.collidepoint(ball.pos[0], ball.pos[1]):
            score1 += 1
            goal_caption_started_at = pygame.time.get_ticks()
            if score1 >= win_score:
                return {"winner": p1_team, "loser": p2_team, "score": (score1, score2)}
            ball.reset()

        p1.draw(screen)
        p2.draw(screen)
        ball.draw(screen)

        t = GOAL_POST_THICKNESS
        pygame.draw.line(screen, WHITE, (0, GOAL_Y), (GOAL_WIDTH, GOAL_Y), t)
        pygame.draw.line(screen, WHITE, (GOAL_WIDTH, GOAL_Y), (GOAL_WIDTH, GROUND_Y), t)
        pygame.draw.line(screen, WHITE, (WIDTH, GOAL_Y), (WIDTH - GOAL_WIDTH, GOAL_Y), t)
        pygame.draw.line(screen, WHITE, (WIDTH - GOAL_WIDTH, GOAL_Y), (WIDTH - GOAL_WIDTH, GROUND_Y), t)

        draw_outlined_text(screen, f"{score1}  :  {score2}", font, WHITE, BLACK, SCORE_TEXT_POS)

        if use_timer:
            timer_label = "GOLDEN BALL!" if is_golden_ball else f"TIME: {int(remaining_time)}s"
            draw_outlined_text(screen, timer_label, font, WHITE, BLACK, (WIDTH // 2, 100), center=True)

        draw_outlined_text(screen, p1.team_name, name_font, WHITE, BLACK, (20, 24))
        p2_label_w = name_font.size(p2.team_name)[0]
        draw_outlined_text(screen, p2.team_name, name_font, WHITE, BLACK, (WIDTH - p2_label_w - 20, 24))

        pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)
        draw_gear_button(screen, gear_font)

        if goal_caption_started_at is not None:
            if not draw_goal_caption(screen, goal_caption_font, goal_caption_started_at):
                goal_caption_started_at = None

        pygame.display.flip()