from ..functions.remaining_stones import remaining_stones
from ..classes.board import Board
from ..classes.color import Color
from ..classes.stone import Stone
import numpy as np
import sys
from ..functions.check_win import check_winning
from ..functions.possible_moves import possible_moves
from ..functions.scoring import scoring


def minimax(
    board: Board,
    depth: int,
    alpha: int,
    beta: int,
    player_color: Color,
    opponent_color: Color,
    maximizing: bool
) -> tuple[int, Board]:
    """
    This is an implementation of a classical minimax function with alpha-beta pruning.
    It tries to find the best possible move for the player
    :param board: actual board state
    :param depth: actual search depth
    :param alpha: alpha value for pruning
    :param beta: beta value for pruning
    :param player_color: color of player who's turn it is
    :param opponent_color: opponents player color
    :return: best possible move
    """

    # if no move is possible return -100 and the board
    stones = remaining_stones(board)
    possible_moves_list = list(
        set(possible_moves(board, stones[(player_color, False)], stones[(player_color, True)], player_color))
    )

    if len(possible_moves_list) == 0:
        return -100, board

    # if maximum depth is reached the board state gets evaluated
    if depth == 0:
        return scoring(board, player_color, stones), board

    # initialize the best move
    best_move = possible_moves_list[0]

    # player tries so maximize the score
    if maximizing:
        maxEval = -sys.maxsize
        for move in possible_moves_list:

            # player won, directly return very high score
            player_won, _ = check_winning(move, player_color)
            if player_won:
                return +1000, move

            # opponent won directly return very low score
            opponent_won, _ = check_winning(move, opponent_color)
            if opponent_won:
                return -1000, move

            eval, _ = minimax(
                move, depth - 1, alpha, beta, opponent_color, player_color, False
            )
            if eval > maxEval:
                maxEval = eval
                best_move = move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval, best_move

    # player tries to minimize the score
    else:
        minEval = +sys.maxsize
        for move in possible_moves_list:

            # player won, directly return very high score
            player_won, _ = check_winning(move, player_color)
            if player_won:
                return +1000, move

            # opponent won directly return very low score
            opponent_won, _ = check_winning(move, opponent_color)
            if opponent_won:
                return -1000, move

            eval, _ = minimax(
                move, depth - 1, alpha, beta, opponent_color, player_color, True
            )
            if eval < minEval:
                minEval = eval
                best_move = move
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        return minEval, best_move
