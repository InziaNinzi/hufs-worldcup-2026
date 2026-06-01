import sys

import pygame

from src.constants import (
    HEIGHT,
    STATE_PLAYING,
    STATE_RESULT,
    STATE_SELECTION,
    STATE_TITLE,
    TITLE,
    WIDTH,
)
from src.game import run_match
from src.result_screen import ResultScreen
from src.selection_menu import SelectionMenu
from src.title_screen import TitleScreen


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    title_screen = TitleScreen()
    selection_menu = SelectionMenu()
    result_screen = ResultScreen()
    state = STATE_TITLE
    selected_teams = None
    match_result = None

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

            selected_teams = [teams["p1"], teams["p2"]]
            state = STATE_PLAYING

        elif state == STATE_PLAYING:
            match_result = run_match(
                screen,
                clock,
                selected_teams[0],
                selected_teams[1],
            )
            if match_result is False:
                break
            if match_result is True:
                state = STATE_SELECTION
                continue
            state = STATE_RESULT

        elif state == STATE_RESULT:
            next_state = result_screen.run(
                screen,
                clock,
                match_result,
                selected_teams,
            )
            if next_state is None:
                break
            state = STATE_SELECTION

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
