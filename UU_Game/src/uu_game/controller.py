import copy
import curses
import argparse
from typing import Optional
from uu_game.vec2 import Vec2
from uu_game.model.game import Game, PlayerSpec
from uu_game.model.stone import Stone, StonePose
from uu_game.views.hand_view import HandView
from uu_game.views.common import set_background
from uu_game.views.boxes_view import BoxesView
from uu_game.views.error_view import ErrorInfo, ErrorView
from uu_game.views.instructions_view import InstructionsView
from uu_game.views.unicode_board_view import UnicodeBoardView
from uu_game.curses_wrappers import start_curses, exit_curses
from uu_game.views.button_view import ButtonView
from b.uugame_ai.classes.mode import Mode # type: ignore
from b.uugame_ai.main import run_ai_compat
from uu_game.views.view import View # type: ignore


parser = argparse.ArgumentParser()
parser.add_argument("--player1", default="human", type=str, choices=["human", "easy", "medium", "hard"])
parser.add_argument("--player2", default="human", type=str, choices=["human", "easy", "medium", "hard"])
parser.add_argument("--first", default="black", type=str, choices=["white", "black"])
args = parser.parse_args()
difficulty_map = {"easy": Mode.EASY, "medium": Mode.MEDIUM, "hard": Mode.HARD, "human": None}

class Controller:
    def __init__(self, curses_window: curses.window):
        self.curses_window = curses_window
        self.last_pressed: Optional[Vec2] = None
        self.first_move = True
        self.using_keyboard = False

        # Model
        self.game = Game(Vec2(5, 5), 5, [
            PlayerSpec(color=0 if args.first == "black" else 1, ai=difficulty_map[args.player1]),
            PlayerSpec(color=1 if args.first == "black" else 0, ai=difficulty_map[args.player2])
        ])

        self.views = []
        self.init_views()

    def init_views(self):
        self.error_info = ErrorInfo()
        # Views. More advanced layout will be used later, possibly removing
        # some views if they do not fit.
        term_h, term_w = self.curses_window.getmaxyx()
        self.board_view = UnicodeBoardView(
            self.game.board, self.curses_window,
            Vec2((term_w - self.game.board.size.x) // 2, (term_h - self.game.board.size.y) // 2))
        hand_view = HandView(self.game.hand, self.curses_window, self.board_view.offset + Vec2(self.board_view.size.x+1, 0), Vec2(1, 5))
        self.board_cursor = Vec2(self.game.board.size.x // 2, self.game.board.size.x // 2)
        boxes_w = 23
        boxes_h = 4*len(self.game.players)-1
        self.boxes_view = BoxesView(
            self.game.players, self.curses_window,
            self.board_view.offset + Vec2(self.board_view.size.x+4, self.game.board.size.y//2-boxes_h//2),
            Vec2(boxes_w, boxes_h)
            )
        instructions_view = InstructionsView(self.curses_window, Vec2(1, 2))
        entire_width = self.board_view.size.x + hand_view.size.x + self.boxes_view.size.x
        if entire_width - self.board_view.size.x//2 >= term_w//2:
            self.board_view.offset.x = (term_w - entire_width) // 2
            hand_view.offset.x = self.board_view.offset.x + self.board_view.size.x + 1
            self.boxes_view.offset.x = hand_view.offset.x + hand_view.size.x + 1
        entire_width_incl_instructions = entire_width + instructions_view.size.x
        if entire_width_incl_instructions > term_w:
            instructions_view = View(self.curses_window, Vec2(0, 0))
        self.views = [
            instructions_view,
            self.board_view,
            hand_view,
            ErrorView(self.error_info, self.curses_window, Vec2(0, 0)),
            self.boxes_view
            ]

    def run(self):
        """
        Entry point for the entire game (except for the curses cleanup code in case of an exception)
        """
        start_curses(self.curses_window)
        set_background(self.curses_window)
        while True:
            self.render()
            # Wait for user input
            key = self.curses_window.getch()
            vector = Vec2(0, 0)
            if key == curses.KEY_MOUSE:
                _, x, y, _, button_state = curses.getmouse()
                self.on_mouse_click(Vec2(x, y), button_state)
            elif key == curses.KEY_RESIZE:
                self.curses_window.clear()
                self.init_views()
                self.render()
            elif key == curses.KEY_UP or key == ord('w'):
                vector.y = -1
            elif key == curses.KEY_DOWN or key == ord('s'):
                vector.y = 1
            elif key == curses.KEY_LEFT or key == ord('a'):
                vector.x = -1
            elif key == curses.KEY_RIGHT or key == ord('d'):
                vector.x = 1
            elif key == ord("\t"):
                self.select_next_pose()
            elif key == ord(' ') or key == ord('\n'):
                self.on_board_click(self.board_cursor, from_key=True)
            elif key == ord('1') or key == ord('2'):
                new_pose = StonePose.STANDING if key == ord('2') else StonePose.FLAT
                if self.using_keyboard:
                    def game_actions():
                        self.boxes_view.selected_pose = None
                        return self.game.place_from_box(self.board_cursor, new_pose)
                    self.perform_game_actions(game_actions)
                else:
                    if self.can_select_pose(new_pose):
                        if self.boxes_view.selected_pose != new_pose:
                            self.boxes_view.selected_pose = new_pose
                        else:
                            self.boxes_view.selected_pose = None
            elif key == ord('i'):
                self.curses_window.clear()
                # set cursor to 0,0
                self.curses_window.move(0, 0)
                exit_curses(self.curses_window)
                curses.nl()
                curses.noraw()
                print("\n\r".join(
"""This game has a white player and a black player.
The game pieces are called stones and have two types: flat and standing.
This is a flat stone █ and this is a standing stone ●.
A player wins when they have visually connected opposite borders with a road of flat stones.
To count towards a road the stones can’t have another stone on top of tem.
When the board is fully covered and both players have placed all their stones on a flat win occurs. This means that the player with the most visible flat stones wins.
If both players build a full road at the same turn the game comes to a draw.
The black player places the first stone.
For the first turn you place a stone of your opponent’s color from your box.
For the rest of the game you only place stones of your own color.
When it’s your turn you can either place a new stone from your box or pick up a stack of stones from one of the squares on the board.
The bottom stones of a stack can’t be moved. This means that you can only pick up stones from the board if there are more than one stone in the square.
When picking up a stack of stones from the board you can pick up a maximum of 5 stones. When placing these stones you have to place them in an adjacent square. First in an adjacent  square to the square you picked up the stack from. After that an adjacent square to where you last placed a stone until you have placed all the stones you picked up.
You can’t balance stones on a standing stone ● ∴ it prevents stacking.
When making a move you can either use the mouse/keyboard.
With the mouse you can click to select the stone type, pick up stones and drop stones on the board.
Using WASD/↑←↓→ you can choose where to place stones on board.
To select a stone type to place on the board you can press 1 for flat stone and 2 for standing stone.
To drop or pick up a stone press space.
You can suggest a draw at any time after beginning the game.
You can admit defeat after the opponent has denied your draw.
To suggest a draw: Click draw-button/press U: black or T: white.
Answer Yes: Click yes-button/press Y.
Answer No: Click no-button/press N.
To admit a defeat: Click defeat-button/press M
To quit press: Q
To choose which player goes first, and which difficulty the AI should have and the player(s) it will play as, use --help to see the arguments to use when starting the game.

Scroll up to see the full instructions. Press enter to continue.
""".split("\n")))
                input()
                curses.nonl()
                curses.raw()
                start_curses(self.curses_window)
            elif key == ord('q'):
                break
            if self.board_cursor + vector in self.game.board and not (self.first_move and not self.using_keyboard):
                self.board_cursor += vector
            if vector != Vec2(0, 0):
                self.using_keyboard = True
            self.activate_draw_defeat_button(key)

            self.curses_window.refresh()
        exit_curses(self.curses_window)

    def activate_draw_defeat_button(self, key: int):
        def game_actions():
            if key == ord('u'):
                self.game.set_wants_draw(self.game.get_player_of_color(0))
            elif key == ord('t'):
                self.game.set_wants_draw(self.game.get_player_of_color(1))
            elif key == ord('y') or key == ord('n'):
                if any(player.wants_draw for player in self.game.players):
                    for player in self.game.players:
                        if player.wants_draw is None:
                            self.game.set_wants_draw(player, key == ord('y'))
            elif key == ord('m'):
                for player in self.game.players:
                    for opponent in self.game.players:
                        if opponent != player:
                            if opponent.wants_draw == False:
                                self.game.set_accepts_defeat(player)
        self.perform_game_actions(game_actions)

    def on_board_click(self, pos: Vec2, button_flags: int = 0, from_key = False):
        """
        pos: coordiantes relative to top-left corner
        button_flags: See https://docs.python.org/3/library/curses.html#curses.getmouse
        """
        self.using_keyboard = from_key
        self.board_cursor = pos
        if from_key and button_flags == 0:
            self.on_board_click(self.board_cursor, curses.BUTTON1_PRESSED, from_key=True)
            self.on_board_click(self.board_cursor, curses.BUTTON1_RELEASED, from_key=True)
            return
        pressed = button_flags & curses.BUTTON1_PRESSED
        released = button_flags & curses.BUTTON1_RELEASED
        if not ((pressed or released) and pos in self.game.board):
            return
        def game_actions():
            if self.boxes_view.selected_pose:
                pose = self.boxes_view.selected_pose
                self.boxes_view.selected_pose = None
                return self.game.place_from_box(pos, pose)
            elif self.game.is_placing() and (pressed or pos != self.last_pressed):
                return self.game.place_from_hand(pos)
            elif pressed:
                self.game.pick_up(pos)
            elif released and len(self.game.board[pos]) == 0 and self.first_move:
                self.select_next_pose()
                self.error_info.error = "Click in the rightmost box to select which stone to place, or switch with TAB."
        self.perform_game_actions(game_actions)
        if pressed:
            self.last_pressed = pos

    def perform_game_actions(self, func):
        """
        Catch any ValueErrors the game may trigger and displays it in the UI.
        Also activates the AI without leaving the screen unrefreshed.
        """
        try:
            board_copy = copy.deepcopy(self.game.board)
            outcome = func()
            if outcome is not None:
                if outcome == self.game.players:
                    self.error_info.error = "Draw! Press Q to quit."
                elif len(outcome) == 1:
                    winner = self.game.get_player_of_color(outcome[0].color)
                    self.error_info.error = f"{winner.get_name()} won! Press Q to quit."
            self.render()
            self.curses_window.refresh()
            try:
                if run_ai_compat is not None and Mode is not None and self.game.active_player.ai is not None:
                    run_ai_compat(self.game, self.game.active_player.ai)
                    if self.game.outcome is None:
                        self.perform_game_actions(lambda: None)
            except ValueError:
                pass
            if board_copy != self.game.board:
                self.error_info.error = ""
                self.first_move = False
        except ValueError as e:
            self.error_info.error = str(e)

    def can_select_pose(self, pose: StonePose):
        if self.game.is_placing():
            return pose is None
        return self.game.active_player.stone_counts[pose] >= 1

    def select_next_pose(self):
        options = list(filter(lambda pose: self.can_select_pose(pose), StonePose))+[None]
        self.boxes_view.selected_pose = options[options.index(self.boxes_view.selected_pose)-1]

    def on_boxes_click(self, pos: Vec2, button_flags: int):
        """
        x, y: coordinates relative to top-left corner
        button_flags: See https://docs.python.org/3/library/curses.html
        """
        if not (button_flags & curses.BUTTON1_PRESSED):
            return
        if (pos.y - 2) % 4 == 0:
            player_index = (pos.y - 2) // 4
            status_line, keybinds = self.boxes_view.get_player_status_line_and_keybinds(
                self.game.players[player_index],
                self.game.players[(player_index + 1) % 2])
            # Find closest keybind to the cursor
            string_pos = pos.x - 2
            closest_keybind = None
            for keybind in keybinds:
                if closest_keybind is None or abs(string_pos - status_line.index(keybind)) < abs(string_pos - status_line.index(closest_keybind)):
                    closest_keybind = keybind
            if closest_keybind is not None:
                self.activate_draw_defeat_button(ord(closest_keybind.lower()))
        pose = StonePose.STANDING if pos.x >= 5 else StonePose.FLAT
        if self.can_select_pose(pose):
            v = self.boxes_view
            v.selected_pose = None if v.selected_pose == pose else pose

    def on_screen_button_click(self, button: ButtonView, pos: Vec2, event_flags: int):
        if not (event_flags & curses.BUTTON1_PRESSED):
            return
        def game_actions():
            if button.id == "draw":
                self.game.set_wants_draw(self.game.active_player)
            elif button.id == "defeat":
                self.game.set_accepts_defeat(self.game.active_player)
        self.perform_game_actions(game_actions)

    def on_mouse_click(self, term_pos: Vec2, button_flags: int):
        """
        Handle the click based on all views it was within, using positions
        relative to them.
        """
        for view in self.views:
            relative_pos = term_pos - view.offset
            if Vec2(0, 0) <= relative_pos < view.size:
                args = relative_pos, button_flags
                if type(view) == UnicodeBoardView:
                    self.on_board_click(*args)
                elif type(view) == BoxesView:
                    self.on_boxes_click(*args)
                elif type(view) == ButtonView:
                    self.on_screen_button_click(view, *args)

    def render(self):
        """
        Renders all views.
        """
        for view in self.views:
            view.render()
        
        if self.using_keyboard:
            board = self.game.board
            self.board_view.set_char(Vec2(self.board_cursor.x,                  -1), "▼")
            self.board_view.set_char(Vec2(self.board_cursor.x,        board.size.y), "▲")
            self.board_view.set_char(Vec2(                 -1, self.board_cursor.y), "▶")
            self.board_view.set_char(Vec2(       board.size.x, self.board_cursor.y), "◀")
