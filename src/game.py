import pygame

from src.ball import Ball
from src.constants import (
    FPS,
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


def run_match(screen, clock, p1_team, p2_team):
    font = pygame.font.SysFont("malgungothic", 40)
    name_font = pygame.font.SysFont("malgungothic", 22)

    score1, score2 = 0, 0
    p1 = Player(150, 500, P1_CONTROLS, p1_team["color"], PLAYER1_IMAGE_PATH)
    p2 = Player(800, 500, P2_CONTROLS, p2_team["color"], PLAYER2_IMAGE_PATH)
    p1.team_name = p1_team["name"]
    p2.team_name = p2_team["name"]
    ball = Ball()

    goal_left = pygame.Rect(0, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
    goal_right = pygame.Rect(WIDTH - GOAL_WIDTH, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)

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
            dx = ball.pos[0] - player.circle_x
            dy = ball.pos[1] - player.circle_y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if 0 < dist < player.radius + ball.radius:
                nx = dx / dist
                ny = dy / dist
                pv_n = player.vel_x * nx + player.vel_y * ny
                kick = pv_n * 1.5 + 8
                ball.vel[0] = nx * kick
                ball.vel[1] = ny * kick - 5
                overlap = player.radius + ball.radius - dist
                ball.pos[0] += nx * (overlap + 1)
                ball.pos[1] += ny * (overlap + 1)

        if goal_left.collidepoint(ball.pos[0], ball.pos[1]):
            score2 += 1
            ball.reset()
        if goal_right.collidepoint(ball.pos[0], ball.pos[1]):
            score1 += 1
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

        pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)
        pygame.display.flip()

    return False
