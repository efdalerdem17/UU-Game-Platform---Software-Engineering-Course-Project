from typing import Union
from uu_game.model.stone import Stone, StonePose
from uu_game.model.board import Board
from uu_game.vec2 import Vec2
from .common import TEXT_COLOR
from .view import View

BOARD_COLORS = ["#855d3a", "#b08744"]
PLAYER_COLORS = ["#303030", "#c4c4c4"]
PLAYER_RECENT_COLORS = ["#000000", "#ffffff"]

def get_stone_color(stone: Stone) -> str:
    return PLAYER_RECENT_COLORS[stone.color] if stone.recent else PLAYER_COLORS[stone.color]

def get_stone_char_and_color(top: Stone, below_top: Union[Stone, str]) -> tuple[str, tuple[str, str]]:
    """
    A top-down view of at most two stacked stones
    """
    top_color = get_stone_color(top)
    if type(below_top) == Stone:
        below_top_color = get_stone_color(below_top)
    else:
        assert type(below_top) == str
        below_top_color = below_top

    if top.pose == StonePose.STANDING:
        #if type(below_top) == Stone and top.color == below_top.color:
        # This won't work for low vision players
        if below_top_color == top_color:
            char = '○'
            top_color = PLAYER_COLORS[top.color-1]
        else:
            char = '●'
    else:
        char = '█'
    return char, (top_color, below_top_color)

class UnicodeBoardView(View):
    """
    Renders the board as a top-down pseudo-graphical representation.
    """
    def __init__(self, board: Board, *args):
        super().__init__(*args)
        self.size = board.size
        self.board = board

    def render(self):
        """
        Called by the controller to render this view of the board.
        """
        super().render()
        for y in range(self.board.size.y):
            for x in range(self.board.size.x):
                pos = Vec2(x, y)
                board_color = BOARD_COLORS[(x + y) % len(BOARD_COLORS)]
                top = self.board[pos][-1] if len(self.board[pos]) > 0 else None
                if top:
                    under_top = self.board[pos][-2] if len(self.board[pos]) > 1 else None
                    self.set_char(pos, *get_stone_char_and_color(top, under_top or board_color))
                else:
                    self.set_char(pos, ' ', (TEXT_COLOR, board_color))
