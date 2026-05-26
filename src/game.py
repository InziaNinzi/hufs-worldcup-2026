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
    # 타이머 변수 세팅
    total_time = 90
    start_ticks = pygame.time.get_ticks()
    game_over = False
    is_golden_ball = False
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
       # 90초 카운트다운 로직
        # 골든볼 연장전이 아닐 때만 타이머가 작동하도록 조건을 추가합니다.
        if not game_over and not is_golden_ball:
            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            remaining_time = max(0, total_time - seconds_passed)
            
            if remaining_time <= 0:
                if score1 == score2:
                    is_golden_ball = True # 동점이면 연장전
                else:
                    game_over = True # 승패 갈리면 게임 종료
        clock.tick(FPS)
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

       # 게임 오버가 아닐 때만 캐릭터와 공이 움직이도록 제어합니다.
        if not game_over:
            p1.move()
            p2.move()
            ball.update()

            if is_golden_ball and score1 != score2:
                game_over = True
            
           
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
        # 타이머 화면에 그리기
        if is_golden_ball:
            time_text = font.render("GOLDEN BALL!", True, WHITE)
        else:
            time_text = font.render(f"TIME: {int(remaining_time)}s", True, WHITE)
        # 화면의 가로 중앙을 계산하고, 점수판 아래에 타이머를 가운데 정렬합니다.
        timer_rect = time_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(time_text, timer_rect)

        p1_label = name_font.render(p1.team_name, True, WHITE)
        p2_label = name_font.render(p2.team_name, True, WHITE)
        screen.blit(p1_label, (20, 24))
        screen.blit(p2_label, (WIDTH - p2_label.get_width() - 20, 24))

        pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)
        pygame.display.flip()

    return False
