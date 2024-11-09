from enum import Enum


# Note that "pose" was picked instead of "position" to avoid confusion with the
# position of the stone on the board
class StonePose(Enum):
    FLAT = 1
    STANDING = 2

    def __str__(self):
        return "flat" if self == StonePose.FLAT else "standing"

class Stone:
    """
    A piece. Should be treated as immutable.
    """
    def __init__(self, color: int, pose: StonePose):
        self.color = color
        self.pose = pose
        self.recent = False

    def __repr__(self):
        return f"({self.color}, {self.pose})"
    
    # See also unicode_board_view.get_stone_char_and_color
    def __str__(self):
        return f"{self.color} {self.pose}"

    def __eq__(self, other: object):
        return isinstance(other, Stone) and self.color == other.color and self.pose == other.pose

    def __hash__(self):
        return hash((self.color, self.pose))
    
    # Used in match statements. Should match __init__ arguments
    __match_args__ = ("color", "pose")