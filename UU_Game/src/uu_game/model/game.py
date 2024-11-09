from collections import defaultdict, deque
from typing import Optional
from b.uugame_ai.classes.mode import Mode
from uu_game.vec2 import CARDINAL_DIRECTIONS, Vec2
from .board import Board
from .stone import Stone, StonePose

class PlayerSpec:
    def __init__(self, *, color: int, ai: Optional[Mode] = None):
        self.color = color
        self.ai = ai

class Player:
    def __init__(self, spec: PlayerSpec):
        self.color = spec.color
        self.ai = spec.ai
        self.turns = 0
        self.active = False
        self.stone_counts: defaultdict[StonePose, int] = defaultdict(lambda: 0)
        self.stone_counts[StonePose.STANDING] = 5
        self.stone_counts[StonePose.FLAT] = 16
        self.won = False
        self.drew = False
        self.wants_draw: Optional[bool] = None
        self.admits_defeat = False

    def get_color_to_place(self):
        return self.color if self.turns > 0 else (self.color + 1) % 2
    
    def get_total_stone_count(self):
        return sum(self.stone_counts.values())
    
    def get_name(self):
        if self.color == 0:
            return "Black"
        if self.color == 1:
            return "White"
        return f"Player {self.color}"

Outcome = Optional[list[Player]]

class Game:
    """
    The responsiblity of the Game is:
    * turn management
    * win/tie/stalemate conditions
    * intermediate states between moves
    """
    def __init__(self, size: Vec2, hand_limit: int, player_specs: list[PlayerSpec]):
        self.board = Board(size)
        self.players = [Player(spec) for spec in player_specs]
        # self.players.append(Player(2))
        self.active_player = self.players[0]
        self.active_player.active = True
        self.hand: deque[Stone] = deque()
        self.hand_limit = hand_limit
        self.last_updated_cell: Optional[Vec2] = None
        self.outcome: Outcome = None

    def get_max_turns(self):
        return max(self.players, key=lambda x: x.turns).turns

    def get_opponent(self):
        return self.players[(self.players.index(self.active_player) + 1) % len(self.players)]

    def get_player_of_color(self, color: int) -> Player:
        """
        You must not modify the returned player.
        """
        for player in self.players:
            if player.color == color:
                return player
        raise ValueError(f"No player with color {color}")

    def _check_and_apply_flat_win(self):
        """
        Check conditions for flat win
        """
        for player in self.players:
            if player.get_total_stone_count() > 0:
                return
        if self.board.is_completely_covered():
            flat_winning_color = self.board.get_color_with_most_road_parts()
            if flat_winning_color is None:
                raise AssertionError("unreachable")
            self.get_player_of_color(flat_winning_color).won = True

    def _update_outcome(self) -> Outcome:
        road_completers = self.board.get_complete_roads()
        defeat_admitted = any(p.admits_defeat for p in self.players)
        for player in self.players:
            player.won = player.color in road_completers
            if defeat_admitted:
                player.won = not player.admits_defeat
        self._check_and_apply_flat_win()
        if all(p.wants_draw for p in self.players):
            for player in self.players:
                player.won = True
        winners = [p for p in self.players if p.won]
        if len(winners) > 0:
            if len(winners) > 1:
                for winner in winners:
                    winner.drew = True
            self.outcome = winners
            return self.outcome

    def _end_turn(self) -> Outcome:
        """
        Signal that the active player has ended their turn, and make the
        opponent the active player unless the game is determined to be over.
        """
        self.active_player.turns += 1
        outcome = self._update_outcome()
        if outcome is not None:
            return outcome
        self.active_player.active = False
        self.active_player = self.get_opponent()
        self.active_player.active = True

    def _start_turn(self):
        self.board.clear_recent()

    def _place(self, pos: Vec2, stone: Stone):
        self.board[pos].place(stone)
        self.last_updated_cell = pos
        self._check_and_apply_flat_win()

    def set_wants_draw(self, player: Player, value = True) -> Outcome:
        self.assert_no_outcome()
        is_suggesting = not any(p.wants_draw for p in self.players)
        if value == False:
            if is_suggesting:
                raise ValueError(f"{player.get_name()} cannot preemptively reject a draw suggestion")
            player.wants_draw = False
            return None
        if is_suggesting and player.turns == 0:
            raise ValueError(f"{player.get_name()} needs to make a move before suggesting a draw")
        player.wants_draw = True
        return self._update_outcome()

    def set_accepts_defeat(self, player: Player) -> Outcome:
        self.assert_no_outcome()
        if not player.wants_draw or not any(p.wants_draw == False for p in self.players):
            raise ValueError(f"{player.get_name()} must have their draw request rejected before admitting defeat")
        if player.turns == 0:
            raise ValueError(f"{player.get_name()} needs to make a move before admitting defeat")
        player.admits_defeat = True
        return self._update_outcome()

    def assert_no_outcome(self):
        if self.outcome is not None:
            raise ValueError("Game is over")

    def place_from_box(self, pos: Vec2, pose: StonePose) -> Outcome:
        self.assert_no_outcome()
        if self.is_placing():
            raise ValueError("Placing from hand, not from box")
        if self.active_player.stone_counts[pose] < 1:
            raise ValueError(f"No {pose} stones left")
        stack = self.board[pos]
        if not stack.can_place():
            raise ValueError(f"Cannot place a stone on top of a standing stone")
        self._start_turn()
        self._place(pos, Stone(self.active_player.get_color_to_place(), pose))
        self.active_player.stone_counts[pose] -= 1
        return self._end_turn()

    def is_placing(self):
        """
        Is the active player currently placing stones from hand?
        """
        return len(self.hand) > 0

    def place_from_hand(self, pos: Vec2, end_turn: bool = True) -> Outcome:
        self.assert_no_outcome()
        if not self.is_placing():
            raise ValueError("Not placing anything from hand")
        is_adjacent = False
        for dir in CARDINAL_DIRECTIONS + [Vec2(0, 0)]:
            if pos + dir == self.last_updated_cell:
                is_adjacent = True
                break
        if not is_adjacent:
            raise ValueError("Place the stone adjacent to your last placed stone")
        self._place(pos, self.hand[0])
        self.hand.popleft()
        if len(self.hand) == 0 and end_turn:
            return self._end_turn()

    def get_max_pick_up(self, pos: Vec2):
        return min(self.hand_limit, len(self.board[pos])-1)

    def pick_up(self, pos: Vec2, amount: Optional[int] = None):
        self.assert_no_outcome()
        if self.is_placing():
            raise ValueError("Cannot pick up while placing from hand")
        source_stack = self.board[pos]
        if len(source_stack) == 0:
            raise ValueError(f"Nothing to pick up")
        if len(source_stack) == 1:
            raise ValueError("Cannot pick up bottom stone")
        if amount is None:
            amount = self.get_max_pick_up(pos)
        if amount > len(source_stack) - 1:
            raise ValueError(f"Cannot pick up {amount} from {pos}, only {len(source_stack)-1} stones above the bottom one")
        if amount <= 0:
            raise ValueError("Must pick up at least one stone")
        self._start_turn()
        for _ in range(amount):
            self.hand.appendleft(source_stack.pop())
        self.last_updated_cell = pos