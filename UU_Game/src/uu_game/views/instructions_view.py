from uu_game.vec2 import Vec2
from uu_game.views.common import BACKGROUND_COLOR, BORDER_COLOR
from .view import BORDER_HALF_BLOCKS, View


class InstructionsView(View):
    def __init__(self, *args):
        super().__init__(*args)
        self.instructions = [
            "To win, visually connect opposite borders with █.",
            "Alt. have most visible █s when board is covered.",
            "Do it the same turn as your opponent to draw.",
            "Place 1 █/● a turn or transfer some from a stack.",
            "Transfer ≤5 stones adjacent to/back into a stack.",
            "Bottom stones are stuck to the board.",
            "Can't balance stones on ● ∴ it prevents stacking.",
            "Suggest a draw or admit defeat at any time.",
            "Mouse: click to select type, pick up and drop",
            "WASD/↑←↓→: cursor. MTUYN: underlined buttons",
            "Space: pick up/drop. 1/2: stone type. Q: quit",
            "Press I for full instructions."
        ]
        self.size = Vec2(max(len(line) for line in self.instructions)+5, len(self.instructions))
    
    def render(self):
        super().render()
        for i, line in enumerate(self.instructions):
            self.print(Vec2(1, i), str(i+1) + ". " + line)
