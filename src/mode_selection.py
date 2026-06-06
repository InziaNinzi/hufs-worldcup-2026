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
)

MODES = [
    {
        "id": "tournament",
        "name": "토너먼트",
        "desc1": "준결승 → 결승을 거쳐 챔피언 결정",
        "desc2": "먼저 3골을 넣으면 경기 승리",
    },
    {
        "id": "friendly",
        "name": "친선전",
        "desc1": "1대1 단판 승부",
        "desc2": "먼저 11골을 넣으면 승리",
    },
]


class ModeSelection:
    def __init__(self):
        self.title_font = pygame.font.SysFont("malgungothic", 48, bold=True)
        self.mode_font = pygame.font.SysFont("malgungothic", 36, bold=True)
        self.desc_font = pygame.font.SysFont("malgungothic", 22)
        self.hint_font = pygame.font.SysFont("malgungothic", 22)
        self.selected = 0
        self.time = 0.0

    def run(self, screen, clock):
        self.selected = 0
        self.time = 0.0

        while True:
            dt = clock.tick(FPS) / 1000.0
            self.time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected = (self.selected - 1) % len(MODES)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected = (self.selected + 1) % len(MODES)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return MODES[self.selected]["id"]
                    elif event.key == pygame.K_ESCAPE:
                        return "title"

            self._draw(screen)
            pygame.display.flip()

    def _draw(self, screen):
        for y in range(HEIGHT):
            t = y / HEIGHT
            r = int(DARK_GREEN[0] * (1 - t) + GREEN[0] * t)
            g = int(DARK_GREEN[1] * (1 - t) + GREEN[1] * t)
            b = int(DARK_GREEN[2] * (1 - t) + GREEN[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        pygame.draw.rect(screen, (28, 100, 48), (0, HEIGHT - 60, WIDTH, 60))
        pygame.draw.line(screen, WHITE, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 2)

        bounce = math.sin(self.time * 3) * 5
        title = self.title_font.render("게임 모드 선택", True, GOLD)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80 + bounce)))

        card_w, card_h = 380, 180
        gap = 40
        total_w = card_w * 2 + gap
        start_x = (WIDTH - total_w) // 2
        card_y = 180

        for i, mode in enumerate(MODES):
            x = start_x + i * (card_w + gap)
            rect = pygame.Rect(x, card_y, card_w, card_h)
            selected = i == self.selected

            bg_color = (20, 80, 40) if selected else (15, 55, 28)
            border_color = GOLD if selected else (80, 120, 80)
            pygame.draw.rect(screen, bg_color, rect, border_radius=14)
            pygame.draw.rect(screen, border_color, rect, 3 if selected else 1, border_radius=14)

            name_color = GOLD if selected else WHITE
            name = self.mode_font.render(mode["name"], True, name_color)
            screen.blit(name, name.get_rect(center=(rect.centerx, rect.y + 55)))

            desc1 = self.desc_font.render(mode["desc1"], True, WHITE)
            desc2 = self.desc_font.render(mode["desc2"], True, GRAY)
            screen.blit(desc1, desc1.get_rect(center=(rect.centerx, rect.y + 105)))
            screen.blit(desc2, desc2.get_rect(center=(rect.centerx, rect.y + 135)))

            if selected:
                arrow = self.mode_font.render("▲", True, GOLD)
                screen.blit(arrow, arrow.get_rect(center=(rect.centerx, rect.bottom + 18)))

        hint = self.hint_font.render("←→ / W S  모드 변경    ENTER  선택    ESC  뒤로", True, WHITE)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 30)))
