from collections import defaultdict
from ..classes.board import Board
from ..classes.color import Color
from ..classes.stone import Stone
from ..functions.check_win import check_winning
from ..functions.check_win_next_round import check_winning_next_round


def scoring(board: Board, player_color: Color, stones: dict[tuple[Color, bool], int]) -> int:
    """
    This function calculates a score for a given board state.
    :param board: actual board state
    :param player_color: color of player who's turn it is
    :param stones: dict with stones left for both players
    :return: score of board state
    """
    # initalize score
    score = 0

    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE

    win_next_move_player, _, _ = check_winning_next_round(
        board, player_color, stones[(player_color, False)]
    )
    win_next_move_opponent, _, _ = check_winning_next_round(
        board, opponent_color, stones[(player_color, False)]
    )

    # +500 for chance to win with next move
    if win_next_move_player:
        # print("chance to win")
        score += 500

    # -1000 if opponent could win with next move
    # if the AI chooses this move the opponent will win in next move
    if win_next_move_opponent:
        # print("chance to lose")
        score += -1000

    # stones left
    # zero for 1 and 5 stones left
    # best if 3 stones left
    # -25 otherwise
    total_own_stones = stones[(player_color, False)] + stones[(player_color, False)]
    score += max(-5 * (total_own_stones - 3) ** 2 + 20, -25)

    if total_own_stones == 14:
        score += -40
    elif total_own_stones == 13:
        score += -30
    elif total_own_stones == 12:
        score += -20
    elif total_own_stones == 11:
        score += -10

    # detailed scoring of stacks
    # penelize if standing stone on own flat
    # reward for having stones of own color directly stacked on each other
    # penelize to many standing stones, above three standing stones
    player_stones_on_top = 0
    opponent_stones_on_top = 0
    standing_on_own = 0
    own_color_stacked = 0
    amount_standing = 0
    standing_on_other = 0

    for x in range(board.size.x):
        for y in range(board.size.y):
            cell = board.get_cell(x, y)
            if len(cell) > 0:
                own_color_before = False
                some_stone_before = False
                for stone in cell:
                    if stone.color == player_color:
                        if own_color_before and not stone.is_standing:
                            own_color_stacked += 1
                        if stone.is_standing:
                            amount_standing += 1
                            if own_color_before:
                                standing_on_own += 1
                            elif some_stone_before:
                                standing_on_other += 1
                        own_color_before = True
                    else:
                        own_color_before = False
                        some_stone_before = True
                if not cell[-1].is_standing:
                    if cell[-1].color == player_color:
                        player_stones_on_top += 1
                    else:
                        opponent_stones_on_top += 1

    # ratio of stones on top
    score += (player_stones_on_top - opponent_stones_on_top) * 3

    # standing stones on own or other color
    score += standing_on_own * -20
    score += standing_on_other * 5

    # to many standing stones
    score += min((amount_standing - 3) * -8, 0)

    # own color stacked
    score += own_color_stacked * 15
    # print(score)
    return score
