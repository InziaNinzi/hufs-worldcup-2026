import sys

import pygame

from src.background_selection import BackgroundSelection
from src.constants import (
    FRIENDLY_WIN_SCORE,
    HEIGHT,
    MATCH_WIN_SCORE,
    STATE_BACKGROUND,
    STATE_PLAYING,
    STATE_RESULT,
    STATE_SELECTION,
    STATE_TITLE,
    TITLE,
    TOURNAMENT_TEAMS,
    WIDTH,
)
from src.game import run_match
from src.result_screen import ResultScreen
from src.selection_menu import SelectionMenu
from src.victory_screen import run_victory_screen
from src.title_screen import TitleScreen


def build_semifinal_bracket(match_result, selected_teams):
    selected_ids = {team["id"] for team in selected_teams}
    remaining_teams = [
        team for team in TOURNAMENT_TEAMS
        if team["id"] not in selected_ids
    ]

    if not remaining_teams:
        remaining_teams = [match_result["loser"]]

    return {
        "semi_1": selected_teams,
        "semi_1_winner": match_result["winner"],
        "semi_2": remaining_teams,
        "semi_2_winner": None,
        "final": [match_result["winner"]],
        "champion": None,
    }


def build_final_bracket(previous_bracket, match_result, selected_teams):
    bracket = previous_bracket.copy()
    bracket["semi_2_winner"] = selected_teams[1]
    bracket["final"] = selected_teams
    bracket["champion"] = match_result["winner"]
    return bracket


def reset_tournament():
    return {
        "mode": "tournament",
        "selected_teams": None,
        "match_result": None,
        "bracket": None,
        "locked_winner_team": None,
        "final_candidate_teams": None,
        "is_final_match": False,
        "selected_background": None,
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    title_screen = TitleScreen()
    background_selection = BackgroundSelection()
    selection_menu = SelectionMenu()
    result_screen = ResultScreen()
    state = STATE_TITLE
    tournament = reset_tournament()

    while True:
        if state == STATE_TITLE:
            mode = title_screen.run(screen, clock)
            if mode is None:
                break
            tournament = reset_tournament()
            tournament["mode"] = mode
            state = STATE_BACKGROUND

        elif state == STATE_BACKGROUND:
            selected_background = background_selection.run(screen, clock)
            if selected_background is None:
                break
            if selected_background == "title":
                tournament = reset_tournament()
                state = STATE_TITLE
                continue
            tournament["selected_background"] = selected_background
            state = STATE_SELECTION

        elif state == STATE_SELECTION:
            teams = selection_menu.run(
                screen,
                clock,
                tournament["locked_winner_team"],
                tournament["final_candidate_teams"],
            )
            if teams is None:
                break
            if teams == "title":
                tournament = reset_tournament()
                state = STATE_TITLE
                continue
            if teams == "selection":
                tournament = reset_tournament()
                state = STATE_SELECTION
                continue

            tournament["selected_teams"] = [teams["p1"], teams["p2"]]
            state = STATE_PLAYING

        elif state == STATE_PLAYING:
            selected_teams = tournament["selected_teams"]
            is_friendly = tournament["mode"] == "friendly"
            match_result = run_match(
                screen,
                clock,
                selected_teams[0],
                selected_teams[1],
                tournament["selected_background"],
                win_score=FRIENDLY_WIN_SCORE if is_friendly else MATCH_WIN_SCORE,
                use_timer=not is_friendly,
            )

            if match_result == "quit" or match_result is False:
                break
            if match_result == "title":
                tournament = reset_tournament()
                state = STATE_TITLE
                continue
            if not isinstance(match_result, dict):
                break

            tournament["match_result"] = match_result

            if is_friendly:
                vr = run_victory_screen(screen, clock, match_result["winner"])
                if vr is None:
                    break
                tournament = reset_tournament()
                state = STATE_TITLE
                continue

            if tournament["is_final_match"]:
                tournament["bracket"] = build_final_bracket(
                    tournament["bracket"],
                    match_result,
                    selected_teams,
                )
                vr = run_victory_screen(screen, clock, match_result["winner"])
                if vr is None:
                    break
            else:
                tournament["bracket"] = build_semifinal_bracket(
                    match_result,
                    selected_teams,
                )
            state = STATE_RESULT

        elif state == STATE_RESULT:
            next_state = result_screen.run(
                screen,
                clock,
                tournament["match_result"],
                tournament["bracket"],
                tournament["is_final_match"],
            )
            if next_state is None:
                break
            if next_state == "final_selection":
                tournament["locked_winner_team"] = (
                    tournament["match_result"]["winner"]
                )
                tournament["final_candidate_teams"] = tournament["bracket"]["semi_2"]
                tournament["is_final_match"] = True
                state = STATE_SELECTION
                continue

            tournament = reset_tournament()
            state = next_state

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
