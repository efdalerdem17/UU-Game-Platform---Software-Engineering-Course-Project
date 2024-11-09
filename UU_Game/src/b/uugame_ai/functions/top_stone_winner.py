from typing import Optional
from ..classes.board import Board
from ..classes.color import Color


def top_stone_winner(board_state: Board) -> Optional[Color]:

    # number of stones in the board
    black_stone_count = 0
    white_stone_count = 0

    # traversing the each cell of the board
    for x in range(board_state.size.x):
        for y in range(board_state.size.y):
            if board_state.get_cell(x, y)[-1].is_standing == True:
                continue
            if board_state.get_cell(x, y)[-1].color == Color.BLACK:
                black_stone_count += 1
            else:
                white_stone_count += 1

    if black_stone_count == white_stone_count:
        return None

    if black_stone_count > white_stone_count:
        return Color.BLACK
    else:
        return Color.WHITE
