import pygame

from src.constants import (
    FPS,
    GOLD,
    GRAY,
    GREEN,
    HEIGHT,
    LIGHT_GRAY,
    PLAYER_SIZE,
    TOURNAMENT_TEAMS,
    WHITE,
    WIDTH,
)


class SelectionMenu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("malgungothic", 42, bold=True)
        self.label_font = pygame.font.SysFont("malgungothic", 28)
        self.team_font = pygame.font.SysFont("malgungothic", 32, bold=True)
        self.hint_font = pygame.font.SysFont("malgungothic", 22)
        self.p1_index = 0
        self.p2_index = 1
        self.p1_ready = False
        self.p2_ready = False

    def run(self, screen, clock):
        self.p1_index = 0
        self.p2_index = min(1, len(TOURNAMENT_TEAMS) - 1)
        self.p1_ready = False
        self.p2_ready = False

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

    def _handle_key(self, key):
        if key == pygame.K_ESCAPE:
            return "title"

        if not self.p1_ready:
            if key == pygame.K_w:
                self.p1_index = (self.p1_index - 1) % len(TOURNAMENT_TEAMS)
            elif key == pygame.K_s:
                self.p1_index = (self.p1_index + 1) % len(TOURNAMENT_TEAMS)
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.p1_ready = True
                if self.p2_index == self.p1_index:
                    self._move_p2_index(1)
            return None

        if not self.p2_ready:
            if key == pygame.K_UP:
                self._move_p2_index(-1)
            elif key == pygame.K_DOWN:
                self._move_p2_index(1)
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.p2_index != self.p1_index:
                    self.p2_ready = True
            return None

        if key in (pygame.K_RETURN, pygame.K_SPACE):
            return {
                "p1": TOURNAMENT_TEAMS[self.p1_index],
                "p2": TOURNAMENT_TEAMS[self.p2_index],
            }
        return None

    def _move_p2_index(self, direction):
        self.p2_index = (self.p2_index + direction) % len(TOURNAMENT_TEAMS)
        while self.p2_index == self.p1_index:
            self.p2_index = (self.p2_index + direction) % len(TOURNAMENT_TEAMS)

    def _draw(self, screen):
        screen.fill(GREEN)
        pygame.draw.rect(screen, (28, 100, 48), (0, HEIGHT - 60, WIDTH, 60))

        title = self.title_font.render("팀 선택", True, GOLD)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))

        self._draw_panel(screen, 80, "1P", self.p1_index, self.p1_ready, True)
        self._draw_panel(screen, WIDTH // 2 + 40, "2P", self.p2_index, self.p2_ready, False)
        self._draw_vs(screen)
        self._draw_hints(screen)

    def _draw_panel(self, screen, x, label, team_index, ready, is_p1):
        panel_w, panel_h = 380, 380
        panel = pygame.Rect(x, 120, panel_w, panel_h)
        border_color = GOLD if ready else WHITE
        pygame.draw.rect(screen, (20, 70, 35), panel, border_radius=12)
        pygame.draw.rect(screen, border_color, panel, 3, border_radius=12)

        label_surf = self.label_font.render(label, True, GOLD if is_p1 else LIGHT_GRAY)
        screen.blit(label_surf, (panel.centerx - label_surf.get_width() // 2, panel.y + 16))

        team = TOURNAMENT_TEAMS[team_index]
        preview_x = panel.centerx - PLAYER_SIZE[0] // 2
        preview_y = panel.centery - 20
        preview = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        preview.fill(team["color"])
        if team["color"] == (255, 255, 255):
            pygame.draw.rect(preview, GRAY, preview.get_rect(), 2)
        screen.blit(preview, (preview_x, preview_y))

        name_surf = self.team_font.render(team["name"], True, WHITE)
        screen.blit(name_surf, (panel.centerx - name_surf.get_width() // 2, panel.bottom - 70))

        status = "선택 완료 ✓" if ready else "팀 고르는 중..."
        status_color = GOLD if ready else GRAY
        status_surf = self.hint_font.render(status, True, status_color)
        screen.blit(status_surf, (panel.centerx - status_surf.get_width() // 2, panel.bottom - 38))

    def _draw_vs(self, screen):
        vs_font = pygame.font.SysFont("malgungothic", 48, bold=True)
        vs = vs_font.render("VS", True, WHITE)
        screen.blit(vs, vs.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    def _draw_hints(self, screen):
        if not self.p1_ready:
            hint = "1P: W/S 팀 변경 · SPACE/ENTER 확정"
        elif not self.p2_ready:
            hint = "2P: ↑/↓ 팀 변경 · ENTER 확정"
        else:
            hint = "SPACE/ENTER — 경기 시작  |  ESC — 타이틀로"

        surf = self.hint_font.render(hint, True, WHITE)
        screen.blit(surf, surf.get_rect(center=(WIDTH // 2, HEIGHT - 28)))
