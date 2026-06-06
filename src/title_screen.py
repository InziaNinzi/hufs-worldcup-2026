import math
import pygame

from src.constants import (
    DARK_GREEN,
    FPS,
    GOLD,
    GRAY,
    GREEN,
    HEIGHT,
    WHITE,
    WIDTH,
    YELLOW,
)

_MODES = [
    ("tournament", "토너먼트"),
    ("friendly",   "친선전"),
]


class TitleScreen:
    def __init__(self):
        self.title_font  = pygame.font.SysFont("malgungothic", 64, bold=True)
        self.sub_font    = pygame.font.SysFont("malgungothic", 28)
        self.mode_large  = pygame.font.SysFont("malgungothic", 40, bold=True)
        self.mode_small  = pygame.font.SysFont("malgungothic", 26)
        self.hint_font   = pygame.font.SysFont("malgungothic", 24)
        self.time = 0.0
        self.ball_angle = 0.0
        self.selected = 0

    def run(self, screen, clock):
        self.selected = 0
        self.time = 0.0
        self.ball_angle = 0.0

        while True:
            dt = clock.tick(FPS) / 1000.0
            self.time += dt
            self.ball_angle += dt * 2.5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected = (self.selected - 1) % len(_MODES)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected = (self.selected + 1) % len(_MODES)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return _MODES[self.selected][0]
                    elif event.key == pygame.K_ESCAPE:
                        return None

            self._draw(screen)
            pygame.display.flip()

    def _draw(self, screen):
        self._draw_background(screen)
        self._draw_decorations(screen)
        self._draw_text(screen)

    def _draw_background(self, screen):
        for y in range(HEIGHT):
            t = y / HEIGHT
            r = int(DARK_GREEN[0] * (1 - t) + GREEN[0] * t)
            g = int(DARK_GREEN[1] * (1 - t) + GREEN[1] * t)
            b = int(DARK_GREEN[2] * (1 - t) + GREEN[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        pygame.draw.rect(screen, (28, 100, 48), (0, HEIGHT - 80, WIDTH, 80))
        pygame.draw.line(screen, WHITE, (0, HEIGHT - 80), (WIDTH, HEIGHT - 80), 3)

    def _draw_decorations(self, screen):
        cx, cy = WIDTH // 2, HEIGHT // 2 - 40
        orbit_r = 120
        bx = cx + math.cos(self.ball_angle) * orbit_r
        by = cy + math.sin(self.ball_angle) * orbit_r * 0.35
        pygame.draw.circle(screen, YELLOW, (int(bx), int(by)), 18)
        pygame.draw.circle(screen, WHITE, (int(bx), int(by)), 18, 2)

        for i in range(3):
            x = 80 + i * 120
            pygame.draw.rect(screen, (200, 16, 46),  (x, HEIGHT - 130, 50, 70), border_radius=4)
            pygame.draw.rect(screen, (0, 35, 149), (WIDTH - 130 - i * 120, HEIGHT - 130, 50, 70), border_radius=4)

    def _draw_text(self, screen):
        bounce = math.sin(self.time * 3) * 6
        title_surf = self.title_font.render("2026 북중미 월드컵", True, GOLD)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 140 + bounce)))

        sub_surf = self.sub_font.render("HEAD SOCCER", True, WHITE)
        screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, 210)))

        # 모드 선택
        base_y = 330
        for i, (_, label) in enumerate(_MODES):
            selected = i == self.selected
            font  = self.mode_large if selected else self.mode_small
            color = GOLD if selected else GRAY
            surf  = font.render(label, True, color)
            rect  = surf.get_rect(center=(WIDTH // 2, base_y + i * 58))
            screen.blit(surf, rect)

            if selected:
                arrow_l = self.mode_small.render("◀", True, GOLD)
                arrow_r = self.mode_small.render("▶", True, GOLD)
                screen.blit(arrow_l, (rect.left - arrow_l.get_width() - 10, rect.centery - arrow_l.get_height() // 2))
                screen.blit(arrow_r, (rect.right + 10, rect.centery - arrow_r.get_height() // 2))

        if int(self.time * 2) % 2 == 0:
            hint = self.hint_font.render("↑↓  모드 선택   ENTER  게임 시작", True, WHITE)
            screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 40)))
