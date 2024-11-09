from uu_game.vec2 import Vec2
from uu_game.model.game import Game
from .view import View
from .common import BACKGROUND_COLOR, BORDER_COLOR, SELECTED_TEXT_COLOR, TEXT_COLOR

BUTTON_BACKGROUND_COLOR = "#C02F1D"

class ButtonView(View):
    def __init__(self, text: str, id: str, *args):
        super().__init__(*args)
        self.default_colors = (TEXT_COLOR, BUTTON_BACKGROUND_COLOR)
        self.text = text
        self.id = id
        self.size = Vec2((max(len(line) for line in self.text)+6), int(len(self.text)+6))
    
    def render(self):
        self.print(Vec2(0,0), self.text)
