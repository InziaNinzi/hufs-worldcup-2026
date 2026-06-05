import os

import pygame

from src.constants import (
    DARK_GREEN,
    FPS,
    GOLD,
    GRAY,
    GREEN,
    HEIGHT,
    STADIUM_BACKGROUNDS,
    WHITE,
    WIDTH,
)


class BackgroundSelection:
    def __init__(self):
        self.title_font = pygame.font.SysFont("malgungothic", 42, bold=True)
        self.name_font = pygame.font.SysFont("malgungothic", 30, bold=True)
        self.hint_font = pygame.font.SysFont("malgungothic", 22)
        self.selected_index = 0
        self.preview_images = {}

    def run(self, screen, clock):
        self.selected_index = 0
        self._load_previews()

        while True:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    result = self._handle_key(event.key)
                    if result is not None:
                        return result

            self._draw(screen)
            pygame.display.flip()

    def _load_previews(self):
        self.preview_images = {}
        for background in STADIUM_BACKGROUNDS:
            if not os.path.exists(background["path"]):
                continue

            image = pygame.image.load(background["path"]).convert()
            self.preview_images[background["id"]] = pygame.transform.scale(
                image,
                (250, 150),
            )

    def _handle_key(self, key):
        if key == pygame.K_ESCAPE:
            return "title"
        if key in (pygame.K_a, pygame.K_LEFT):
            self.selected_index = (self.selected_index - 1) % len(
                STADIUM_BACKGROUNDS
            )
        elif key in (pygame.K_d, pygame.K_RIGHT):
            self.selected_index = (self.selected_index + 1) % len(
                STADIUM_BACKGROUNDS
            )
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            return STADIUM_BACKGROUNDS[self.selected_index]
        return None

    def _draw(self, screen):
        screen.fill(DARK_GREEN)
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 70, WIDTH, 70))

        title = self.title_font.render("경기장 배경 선택", True, GOLD)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 55)))

        start_x = 80
        card_gap = 40
        card_width = 280

        for index, background in enumerate(STADIUM_BACKGROUNDS):
            x = start_x + index * (card_width + card_gap)
            selected = index == self.selected_index
            self._draw_background_card(screen, background, x, 145, selected)

        hint = self.hint_font.render(
            "A/D 또는 ←/→ 배경 변경 · SPACE/ENTER 확정 · ESC 타이틀",
            True,
            WHITE,
        )
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 34)))

    def _draw_background_card(self, screen, background, x, y, selected):
        card = pygame.Rect(x, y, 280, 300)
        border_color = GOLD if selected else WHITE
        pygame.draw.rect(screen, (20, 70, 35), card, border_radius=10)
        pygame.draw.rect(screen, border_color, card, 3, border_radius=10)

        preview_rect = pygame.Rect(card.x + 15, card.y + 25, 250, 150)
        preview = self.preview_images.get(background["id"])
        if preview:
            screen.blit(preview, preview_rect)
        else:
            pygame.draw.rect(screen, GRAY, preview_rect)

        pygame.draw.rect(screen, WHITE, preview_rect, 2)

        name = self.name_font.render(background["name"], True, GOLD)
        screen.blit(name, name.get_rect(center=(card.centerx, card.y + 220)))

        status = "선택됨" if selected else " "
        status_surf = self.hint_font.render(status, True, WHITE)
        screen.blit(
            status_surf,
            status_surf.get_rect(center=(card.centerx, card.y + 260)),
        )
