from collections import defaultdict
import copy
from typing import Optional, Union
import sys
from concurrent.futures import ProcessPoolExecutor, TimeoutError
import argparse
from collections import deque
import random
import numpy as np

import uu_game.model.game
from uu_game.model.stone import Stone as AStone, StonePose
from uu_game.vec2 import Vec2
from .classes.stone import Stone
from .classes.color import Color
from .classes.board import Board
from .classes.mode import Mode
from .functions.initial_stone import place_initial_stone
from .functions.validity import is_board_valid
from .functions.check_win import check_winning
from .functions.check_win_next_round import check_winning_next_round
from .functions.possible_moves import possible_moves
from .functions.minimax import minimax
from .functions.top_stone_winner import top_stone_winner
from uu_game.model.board import Board as ABoard

def print(*args):
    pass

def run_ai(board: Board, turn_number: int, player_color: Color, mode: Mode, game: "uu_game.model.game.Game") -> Optional[tuple[bool, Board]]:

    # if the mode is medium change it with 50/50 prob to easy or hard
    if mode == Mode.MEDIUM:
        mode = random.choice([Mode.EASY, Mode.HARD])

    # define opponent color
    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE

    # check if board is valid
    # IsBoardValid = is_board_valid(board, player_color)
    # if not IsBoardValid:
    #     print("invalid board")
    #     return None  # return with error

    # check if initial move
    if game.active_player.turns == 0:
        final_move = place_initial_stone(board, opponent_color)
        print("take initial move")
        print(final_move)
        return False, final_move

    # check if AI won -> should never happen
    # player_won, path = check_winning(board, player_color)
    # if player_won:
    #     print("THE AI WON THE GAME")
    #     print(path)
    #     return True, board

    # # check IF human won
    # opponent_won, path = check_winning(board, opponent_color)
    # if opponent_won:
    #     print("THE HUMAN WON THE GAME")
    #     print(path)
    #     return True, board

    # calculate all possible moves
    possible_moves_list = possible_moves(board, game.active_player.stone_counts[StonePose.FLAT], game.active_player.stone_counts[StonePose.STANDING], player_color)
    print(f"Possible moves: {len(possible_moves_list)}")
    if len(possible_moves_list) == 0:
        game.set_wants_draw(game.active_player, True)
        game.set_wants_draw(game.get_opponent(), True)
        game.set_accepts_defeat(game.active_player)
        # print("no more possible moves")

        # winner_color = top_stone_winner(board)
        # if winner_color == None:
        #     print("DRAW")
        # elif winner_color == player_color:
        #     print("THE AI WON THE GAME")
        # else:
        #     print("THE HUMAN WON THE GAME")

        return True, board # return with unmodified board

    # Start to do one move in easy mode
    if mode == Mode.EASY:

        # choose a random move. If there is a better, more specific one to choose this variable gets overwritten
        final_move = random.choice(possible_moves_list)

        # check if player could finish the game in this round
        win_next_player, _, _ = check_winning_next_round(
            board, player_color, game.active_player.stone_counts[StonePose.FLAT]
        )
        if win_next_player:
            print("Player could win with next move")
            prob_1 = np.random.uniform(0.0, 1.0)
            # with prob 50% the player takes the winning move
            if prob_1 > 0.5:
                print("choose winning option")
                # iterate over all possible moves and find a move that ends the game
                for move in possible_moves_list:
                    player_won, path = check_winning(move, player_color)
                    if player_won:
                        final_move = move
                        break

        else:
            # check if the opponent could win in the next round
            # this function checks just "easy" ways to win the game (place stone or move a stack one cell)
            win_next_opponent, path, foi = check_winning_next_round(
                board, opponent_color, game.get_opponent().stone_counts[StonePose.FLAT]
            )
            if win_next_opponent:
                print("Opponent could win with next move")
                # print(f"Winning path would be: {path}")
                # print(f"FOI is {foi}")
                prob_2 = np.random.uniform(0.0, 1.0)
                # with a probability of 1/4 the player tries to defend it
                if prob_2 > 0.75:
                    print("try to defend")
                    # iterate over all possible moves and find a move that prevents the opponent from winning
                    for move in possible_moves_list:
                        win_next_opponent, _, _ = check_winning_next_round(
                            move, opponent_color, game.get_opponent().stone_counts[StonePose.FLAT]
                        )
                        if not win_next_opponent:
                            final_move = move
                            break
        print(final_move)

    elif mode == Mode.HARD:
        with ProcessPoolExecutor(max_workers=1) as executor:
            future = executor.submit(minimax, board, 3, -sys.maxsize, sys.maxsize, player_color, opponent_color, True)
            try:
                final_score, final_move = future.result() # timeout=4.5
                print("score: ", final_score)
            except TimeoutError:
                final_move = random.choice(possible_moves_list)
    else:
        final_move = random.choice(possible_moves_list)

    # check if one of the two players won with this move
    win_after_move_player, path = check_winning(final_move, player_color)
    if win_after_move_player:
        print(f"The winning path is: {path}")
        print("AI WON")
        return True, final_move  # return winning condition

    win_after_move_oppnent, path = check_winning(final_move, opponent_color)
    if win_after_move_oppnent:
        print(f"The winning path is: {path}")
        print("HUMAN WON")
        return True, final_move

    # finish move by returning
    return False, final_move

COLOR_ID_TO_COLOR = [Color.BLACK, Color.WHITE]

def run_ai_compat(game: "uu_game.model.game.Game", mode: Mode) -> bool:
    game._start_turn()
    old_game_board = copy.deepcopy(game.board)
    counts: defaultdict[AStone, int] = defaultdict(lambda: 0)
    board = Board(game.board.size)
    for x in range(game.board.size.x):
        for y in range(game.board.size.y):
            stones = []
            for stone in game.board[Vec2(x, y)].stones:
                stones.append(Stone(COLOR_ID_TO_COLOR[stone.color], stone.pose == StonePose.STANDING))
                counts[stone] -= 1
            board.set_cell(x, y, stones)
    result = run_ai(board, game.active_player.turns, COLOR_ID_TO_COLOR[game.active_player.color], mode, game)
    if result is not None:
        new_board = result[1]
        for x in range(game.board.size.x):
            for y in range(game.board.size.y):
                stones = deque()
                for stone in new_board.get_cell(x, y):
                    stone = AStone(COLOR_ID_TO_COLOR.index(stone.color), StonePose.STANDING if stone.is_standing else StonePose.FLAT)
                    counts[stone] += 1
                    stones.append(stone)
                    game.board[Vec2(x, y)].stones = stones
        for stone, count in counts.items():
            game.active_player.stone_counts[stone.pose] -= count
        # mark recent
        for x in range(game.board.size.x):
            for y in range(game.board.size.y):
                pos = Vec2(x, y)
                if len(game.board[pos]) > len(old_game_board[pos]):
                    peeked = game.board[pos].peek()
                    if peeked is not None:
                        peeked.recent = True
    game._end_turn()
    return False if result is None else result[0]
