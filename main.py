import sys
import pygame

from src.constants import HEIGHT, STATE_SELECTION, STATE_TITLE, TITLE, WIDTH
from src.game import run_match
from src.selection_menu import SelectionMenu
from src.title_screen import TitleScreen


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    title_screen = TitleScreen()
    selection_menu = SelectionMenu()
    state = STATE_TITLE

    while True:
        if state == STATE_TITLE:
            next_state = title_screen.run(screen, clock)
            if next_state is None:
                break
            state = STATE_SELECTION

        elif state == STATE_SELECTION:
            teams = selection_menu.run(screen, clock)
            if teams is None:
                break
            if teams == "title":
                state = STATE_TITLE
                continue

            quit_game = not run_match(screen, clock, teams["p1"], teams["p2"])
            if quit_game:
                break
            state = STATE_SELECTION

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
