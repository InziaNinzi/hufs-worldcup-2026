import sys
import pygame

from src.ball import Ball
from src.constants import (
    BLUE,
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
    RED,
    SCORE_TEXT_POS,
    TITLE,
    WHITE,
    WIDTH,
)
from src.player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 40)

    score1, score2 = 0, 0
    p1 = Player(150, 500, P1_CONTROLS, RED, PLAYER1_IMAGE_PATH)
    p2 = Player(800, 500, P2_CONTROLS, BLUE, PLAYER2_IMAGE_PATH)
    ball = Ball()

    goal_left = pygame.Rect(0, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
    goal_right = pygame.Rect(WIDTH - GOAL_WIDTH, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)

    running = True
    while running:
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        p1.move()
        p2.move()
        ball.update()

        for player in (p1, p2):
            if player.rect.collidepoint(ball.pos[0], ball.pos[1]):
                ball.vel[0] = (ball.pos[0] - player.rect.centerx) * 0.5
                ball.vel[1] = -10

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

        score_text = font.render(f"{score1} : {score2}", True, WHITE)
        screen.blit(score_text, SCORE_TEXT_POS)
        pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()