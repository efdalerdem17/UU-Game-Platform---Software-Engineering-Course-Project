from collections import defaultdict, deque
from copy import copy
from itertools import count
from typing import Optional
from uu_game.vec2 import CARDINAL_DIRECTIONS, Vec2
from .stone import Stone, StonePose


class Stack:
    def __init__(self):
        self.stones: deque[Stone] = deque()

    def __len__(self):
        return len(self.stones)
    
    def __getitem__(self, index: int) -> Stone:
        return self.stones[index]

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Stack) and self.stones == value.stones

    def peek(self) -> Optional[Stone]:
        return self.stones[-1] if len(self.stones) > 0 else None

    def can_place(self) -> bool:
        top = self.peek()
        return not (top is not None and top.pose == StonePose.STANDING)

    def place(self, stone: Stone):
        stone_copy = copy(stone)
        stone_copy.recent = True
        self.push(stone_copy)

    def push(self, stone: Stone):
        if not self.can_place():
            raise ValueError("Cannot place a stone on top of a standing stone")
        self.stones.append(stone)

    def pop(self) -> Stone:
        return self.stones.pop()
    
    def get_road_color(self) -> Optional[int]:
        for stone in reversed(self.stones):
            if stone.pose == StonePose.STANDING:
                return None
            if stone.pose == StonePose.FLAT:
                return stone.color
        return None

class Board:
    """
    The responsibility of the Board is:
    * ensure stacks on it are always in a valid state
    * provide operations/queries directly related to the stones on it

    __setitem__ are private.
    """

    def __init__(self, size: Vec2):
        self.size = size
        self.board: dict[Vec2, Stack] = dict()
    
    def clear_recent(self):
        for stack in self.board.values():
            for stone in stack.stones:
                stone.recent = False

    def _search(self, pos: Vec2, color: int, visited: set[Vec2], found: set[Vec2]):
        if pos not in self or self[pos].get_road_color() != color:
            return
        if pos in visited:
            return
        visited.add(pos)
        for dir in CARDINAL_DIRECTIONS:
            if pos.is_on_edge(dir, self.size):
                found.add(dir)
            new_pos = pos + dir
            self._search(new_pos, color, visited, found)

    def get_complete_road(self, pos: Vec2) -> Optional[tuple[int, set[Vec2]]]:
        """
        Are two opposite edges of the board connected using flat stones via
        this position?
        """

        color = self[pos].get_road_color()
        if color is None:
            return None
        visited = set()
        found = set()
        self._search(pos, color, visited, found)
        for dim in [Vec2(1, 0), Vec2(0, 1)]:
            if found.issuperset([dim, -dim]):
                return color, visited

    def get_complete_roads(self) -> set[int]:
        """
        Get which colors form complete roads.
        """
        colors = set()
        # NOTE: Inefficent
        for pos in self.board:
            road = self.get_complete_road(pos)
            if road is not None:
                colors.add(road[0])
        return colors

    def __getitem__(self, pos: Vec2) -> Stack:
        """
        Private.

        Example: board[Vec2(0, 0)][-1] is the top stone on the cell (0, 0)
        """
        if pos in self and pos not in self.board:
            self.board[pos] = Stack()
        return self.board[pos]
    
    def __contains__(self, pos: Vec2) -> bool:
        """
        Private.

        Example: if Vec2(0, 0) in board: ...
        """
        return pos.x >= 0 and pos.x < self.size.x and pos.y >= 0 and pos.y < self.size.y
    
    def __setitem__(self, pos: Vec2, value: Stack):
        self.board[pos] = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Board) and self.size == other.size and self.board == other.board
    
    def is_completely_covered(self) -> bool:
        for x in range(self.size.x):
            for y in range(self.size.y):
                if self.board[Vec2(x, y)].peek() is None:
                    return False
        return True
    
    def get_color_with_most_road_parts(self) -> Optional[int]:
        color_counts: dict[int, int] = defaultdict(lambda: 0)
        for stack in self.board.values():
            stone_color = stack.get_road_color()
            if stone_color is not None:
                color_counts[stone_color] += 1
        return max(color_counts.keys(), key=lambda x: color_counts[x], default=None)