from collections import deque
from uu_game.model.stone import Stone
from uu_game.model.game import Game
from uu_game.vec2 import Vec2
from .view import View
from .common import BORDER_COLOR, TEXT_COLOR
from .boxes_view import BOXES_BACKGROUND_COLOR
from .unicode_board_view import get_stone_char_and_color


HAND_BACKGROUND_COLOR = "#855d3a"
class HandView(View):
    def __init__(self, hand: deque[Stone], *args):
        super().__init__(*args)
        self.hand = hand
        self.default_colors = (TEXT_COLOR, HAND_BACKGROUND_COLOR)
    
    def render(self):
        super().render()
        self.fill("▌", (BORDER_COLOR, BOXES_BACKGROUND_COLOR), (Vec2(-1, 0), Vec2(1, self.size.y)))
        self.set_char(Vec2(0, self.size.y), "▓", (BORDER_COLOR, BOXES_BACKGROUND_COLOR))
        for i, piece in enumerate(self.hand):
            self.set_char(Vec2(0, self.size.y-1-i), *get_stone_char_and_color(piece, HAND_BACKGROUND_COLOR))
        