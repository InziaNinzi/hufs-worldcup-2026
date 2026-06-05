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


class ResultScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("malgungothic", 44, bold=True)
        self.team_font = pygame.font.SysFont("malgungothic", 28, bold=True)
        self.text_font = pygame.font.SysFont("malgungothic", 24)
        self.hint_font = pygame.font.SysFont("malgungothic", 20)

    def run(self, screen, clock, match_result, bracket, is_final=False):
        while True:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "selection"
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return "selection" if is_final else "final_selection"

            self._draw(screen, bracket, match_result, is_final)
            pygame.display.flip()

    def _draw(self, screen, bracket, match_result, is_final):
        screen.fill(DARK_GREEN)
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 70, WIDTH, 70))

        title_text = "Final Result" if is_final else "Tournament Result"
        title = self.title_font.render(title_text, True, GOLD)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 54)))

        score_text = f"{match_result['score'][0]} : {match_result['score'][1]}"
        summary = self.text_font.render(
            f"{match_result['winner']['name']} wins  {score_text}",
            True,
            WHITE,
        )
        screen.blit(summary, summary.get_rect(center=(WIDTH // 2, 100)))

        self._draw_match_box(screen, 80, 170, "Semi Final 1", bracket["semi_1"])
        self._draw_match_box(screen, 80, 360, "Semi Final 2", bracket["semi_2"])
        self._draw_match_box(screen, 620, 265, "Final", bracket["final"])

        self._draw_connector(screen, (350, 240), (620, 315))
        self._draw_connector(screen, (350, 430), (620, 365))

        self._draw_winner_label(screen, 380, 215, bracket["semi_1_winner"])
        if bracket["semi_2_winner"] is not None:
            self._draw_winner_label(screen, 380, 405, bracket["semi_2_winner"])
        if is_final:
            self._draw_champion_label(screen, bracket["champion"])

        hint_text = "SPACE/ENTER: team selection  |  ESC: team selection"
        if not is_final:
            hint_text = "SPACE/ENTER: select final opponent  |  ESC: team selection"
        hint = self.hint_font.render(hint_text, True, GRAY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 34)))

    def _draw_match_box(self, screen, x, y, title, teams):
        box = pygame.Rect(x, y, 270, 130)
        pygame.draw.rect(screen, (18, 90, 46), box, border_radius=8)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=8)

        title_surf = self.hint_font.render(title, True, GOLD)
        screen.blit(title_surf, (box.x + 16, box.y + 12))

        for index, team in enumerate(teams):
            row_y = box.y + 48 + index * 38
            pygame.draw.rect(screen, team["color"], (box.x + 16, row_y, 28, 22))
            team_name = self.team_font.render(team["name"], True, WHITE)
            screen.blit(team_name, (box.x + 56, row_y - 4))

    def _draw_connector(self, screen, start_pos, end_pos):
        mid_x = (start_pos[0] + end_pos[0]) // 2
        pygame.draw.line(screen, WHITE, start_pos, (mid_x, start_pos[1]), 3)
        pygame.draw.line(
            screen,
            WHITE,
            (mid_x, start_pos[1]),
            (mid_x, end_pos[1]),
            3,
        )
        pygame.draw.line(screen, WHITE, (mid_x, end_pos[1]), end_pos, 3)

    def _draw_winner_label(self, screen, x, y, team):
        label = self.hint_font.render(f"Advance: {team['name']}", True, GOLD)
        screen.blit(label, (x, y))

    def _draw_champion_label(self, screen, team):
        champion = self.team_font.render(f"Champion: {team['name']}", True, GOLD)
        screen.blit(champion, champion.get_rect(center=(WIDTH // 2, 150)))
