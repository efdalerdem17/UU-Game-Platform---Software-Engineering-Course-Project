import curses
from typing import Optional
from uu_game.model.game import Player
from uu_game.model.stone import Stone, StonePose
from uu_game.vec2 import Vec2
from .common import BACKGROUND_COLOR, BORDER_COLOR, SELECTED_TEXT_COLOR, TEXT_COLOR
from .unicode_board_view import PLAYER_RECENT_COLORS, get_stone_char_and_color
from .view import BORDER_BALANCED_EDGES2, View


BOXES_BACKGROUND_COLOR = "#855d3a"

class BoxesView(View):
    """
    Renders all the boxes as a number for each type of stone for each player,
    and probably also whose turn it is.
    """

    def __init__(self, players, *args):
        super().__init__(*args)
        self.players: list[Player] = players
        self.selected_pose: Optional[StonePose] = None
        self.default_colors = (TEXT_COLOR, BOXES_BACKGROUND_COLOR)
    
    def render(self):
        super().render()
        self.border(BORDER_BALANCED_EDGES2, (BORDER_COLOR, BACKGROUND_COLOR))
        self.fill("▔", (BORDER_COLOR, BOXES_BACKGROUND_COLOR), (Vec2(0, -1), Vec2(self.size.x, 1)))
        self.fill("▁", (BORDER_COLOR, BOXES_BACKGROUND_COLOR), (Vec2(0, self.size.y), Vec2(self.size.x, 1)))
        base_x = 2
        pos = Vec2(base_x, 0)
        for player in self.players:
            self.print(pos, "" + player.get_name(), (PLAYER_RECENT_COLORS[player.color], BOXES_BACKGROUND_COLOR), bold=True)
            self.set_char(pos - Vec2(base_x, 0), "➔" if player.active else " ", (SELECTED_TEXT_COLOR, BOXES_BACKGROUND_COLOR))
            pos.y += 1
            for pose in [StonePose.FLAT, StonePose.STANDING]:
                stone = Stone(player.get_color_to_place(), pose)
                number_colors = SELECTED_TEXT_COLOR if player.active and self.selected_pose == pose else TEXT_COLOR
                self.print(pos, f"{player.stone_counts[pose]: >2}", (number_colors, BOXES_BACKGROUND_COLOR))
                pos.x += 2
                self.set_char(pos, *get_stone_char_and_color(stone, BOXES_BACKGROUND_COLOR))
                pos.x += 2
            pos.y += 1
            pos.x = base_x
            status_line, keybinds = self.get_player_status_line_and_keybinds(player, self.players[(player.color + 1) % 2])
            for char in status_line:
                set_char_args = {}
                if char in keybinds:
                    set_char_args["underline"] = True
                self.set_char(pos, char, (TEXT_COLOR, BOXES_BACKGROUND_COLOR), **set_char_args)
                pos.x += 1
            pos.x = base_x
            pos.y += 2

    def get_player_status_line_and_keybinds(self, subject: Player, opponent: Player) -> tuple[str, list[str]]:
        # Defining the keybinds here violates MVC, but the coupling is not
        # arbitrary: Consider for example that the view cannot choose words
        # that only contain WASD, as they would conflict with the keys for
        # moving the board cursor.
        if subject.drew:
            return "It's a draw", [] 
        if subject.won:
            return f"You won in {subject.turns} turns!", []
        if opponent.won:
            return "You lost.", []
        if subject.ai and subject.active:
            return "Thinking...", []
        if not subject.ai:
            if opponent.wants_draw and subject.wants_draw is None:
                return "Draw? [Yes] / [No]", ["Y", "N"]
            if opponent.wants_draw == False:
                return "Denied [Admit defeat]", ["m"]
            if subject.wants_draw:
                return "Waiting for opponent", []
            if subject.turns > 0:
                return "[Suggest draw]", (["u"] if subject.color == 0 else ["t"])
        if subject.turns == 0:
            if not subject.active:
                return "Wait your turn.", []
            if subject.get_color_to_place() != subject.color:
                return "Place 1 enemy piece.", []
        return "", []
        
