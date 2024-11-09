from main import run_ai
from classes.Stone import Stone
from classes.color import Color
from classes.board import Board
from classes.mode import Mode
import time
import sys

#sys.tracebacklimit = 0

if __name__ == "__main__":
    board: Board = Board()

    board_2 = Board()
    board_2.get_cell(0, 0).append(Stone(Color.BLACK, False))
    board_2.get_cell(0, 0).append(Stone(Color.BLACK, False))
    #board_2.get_cell(0, 1).append(Stone(Color.BLACK, False))
    board_2.get_cell(0, 2).append(Stone(Color.BLACK, False))
    board_2.get_cell(0, 3).append(Stone(Color.BLACK, False))


    board_3 = Board()
    board_3.get_cell(1, 0).append(Stone(Color.BLACK, False))
    board_3.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_3.get_cell(1, 2).append(Stone(Color.BLACK, False))
    board_3.get_cell(2, 2).append(Stone(Color.BLACK, False))
    board_3.get_cell(3, 2).append(Stone(Color.BLACK, False))
    board_3.get_cell(3, 3).append(Stone(Color.BLACK, False))

    board_4 = Board()
    board_4.get_cell(0, 1).append(Stone(Color.BLACK, False))
    board_4.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_4.get_cell(3, 1).append(Stone(Color.BLACK, False))

    board_5 = Board()
    board_5.get_cell(0, 2).append(Stone(Color.BLACK, False))
    board_5.get_cell(1, 0).append(Stone(Color.BLACK, False))
    board_5.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_5.get_cell(1, 2).append(Stone(Color.BLACK, False))
    board_5.get_cell(1, 3).append(Stone(Color.BLACK, False))
    board_5.get_cell(2, 2).append(Stone(Color.BLACK, False))
    board_5.get_cell(3, 2).append(Stone(Color.BLACK, False))

    board_6 = Board()
    board_6.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_6.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_6.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_6.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_6.get_cell(1, 1).append(Stone(Color.BLACK, False))
    board_6.get_cell(1, 1).append(Stone(Color.BLACK, True))


    game_end = False
    player_color = Color.BLACK
    i = 0
    while not game_end:
        # print(f"Start Move Number {i}")
        # print(f"It is{player_color}'s turn")
        i += 1
        #time.sleep(1)
        game_end, board = run_ai(board, i, player_color, Mode.HARD)
        player_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
