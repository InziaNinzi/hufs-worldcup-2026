import pygame

from src.ball import Ball
from src.constants import (
    FPS,
    BLACK,
    GOLD,
    GOAL_CAPTION_DURATION,
    GOAL_CAPTION_FADE_DURATION,
    GOAL_CAPTION_TEXT,
    GOAL_HEIGHT,
    GOAL_WIDTH,
    GOAL_Y,
    GROUND_Y,
    GREEN,
    HEIGHT,
    P1_CONTROLS,
    P2_CONTROLS,
    PLAYER1_IMAGE_PATH,
    PLAYER2_IMAGE_PATH,
    SCORE_TEXT_POS,
    WHITE,
    WIDTH,
)
from src.player import Player


def draw_goal_caption(screen, font, started_at):
    elapsed_time = pygame.time.get_ticks() - started_at
    if elapsed_time >= GOAL_CAPTION_DURATION:
        return False

    remaining_time = GOAL_CAPTION_DURATION - elapsed_time
    fade_time = min(elapsed_time, remaining_time, GOAL_CAPTION_FADE_DURATION)
    alpha = int(255 * fade_time / GOAL_CAPTION_FADE_DURATION)

    caption = font.render(GOAL_CAPTION_TEXT, True, GOLD)
    shadow = font.render(GOAL_CAPTION_TEXT, True, BLACK)
    caption.set_alpha(alpha)
    shadow.set_alpha(alpha)

    caption_rect = caption.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    shadow_rect = shadow.get_rect(
        center=(caption_rect.centerx + 4, caption_rect.centery + 4)
    )

    screen.blit(shadow, shadow_rect)
    screen.blit(caption, caption_rect)
    return True


def run_match(screen, clock, p1_team, p2_team):
    font = pygame.font.SysFont("malgungothic", 40)
    name_font = pygame.font.SysFont("malgungothic", 22)
    goal_caption_font = pygame.font.SysFont("malgungothic", 96, bold=True)

    score1, score2 = 0, 0
    p1 = Player(150, 500, P1_CONTROLS, p1_team["color"], PLAYER1_IMAGE_PATH)
    p2 = Player(800, 500, P2_CONTROLS, p2_team["color"], PLAYER2_IMAGE_PATH)
    p1.team_name = p1_team["name"]
    p2.team_name = p2_team["name"]
    ball = Ball()

    goal_left = pygame.Rect(0, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
    goal_right = pygame.Rect(WIDTH - GOAL_WIDTH, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
    goal_caption_started_at = None

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

        p1.move()
        p2.move()
        ball.update()

        for player in (p1, p2):
            if player.rect.collidepoint(ball.pos[0], ball.pos[1]):
                rel_x = ball.pos[0] - player.rect.centerx
                ball.vel[0] = player.vel_x * 1.5 + rel_x * 0.2
                ball.vel[1] = player.vel_y * 0.3 - 10
                if rel_x >= 0:
                    ball.pos[0] = player.rect.right + ball.radius
                else:
                    ball.pos[0] = player.rect.left - ball.radius

        if goal_left.collidepoint(ball.pos[0], ball.pos[1]):
            score2 += 1
            goal_caption_started_at = pygame.time.get_ticks()
            ball.reset()
        if goal_right.collidepoint(ball.pos[0], ball.pos[1]):
            score1 += 1
            goal_caption_started_at = pygame.time.get_ticks()
            ball.reset()

        p1.draw(screen)
        p2.draw(screen)
        ball.draw(screen)

        pygame.draw.rect(screen, WHITE, goal_left, 2)
        pygame.draw.rect(screen, WHITE, goal_right, 2)

        score_text = font.render(f"{score1}  :  {score2}", True, WHITE)
        screen.blit(score_text, SCORE_TEXT_POS)

        p1_label = name_font.render(p1.team_name, True, WHITE)
        p2_label = name_font.render(p2.team_name, True, WHITE)
        screen.blit(p1_label, (20, 24))
        screen.blit(p2_label, (WIDTH - p2_label.get_width() - 20, 24))

        if goal_caption_started_at is not None:
            is_caption_visible = draw_goal_caption(
                screen,
                goal_caption_font,
                goal_caption_started_at,
            )
            if not is_caption_visible:
                goal_caption_started_at = None

        pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)
        pygame.display.flip()

    return False
