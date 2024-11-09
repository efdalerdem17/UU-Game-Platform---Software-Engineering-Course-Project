class Vec2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: object):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        raise TypeError("Both operands must be Vec2 instances")

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        raise TypeError("Both operands must be Vec2 instances")

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2(int(self.x * other), int(self.y * other))
        raise TypeError("Operand must be an Vec2 instance or a number")

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __repr__(self):
        return f"↗({self.x}, {self.y})"
    
    def __gt__(self, other):
        return isinstance(other, Vec2) and self.x > other.x and self.y > other.y
    
    def __lt__(self, other):
        return isinstance(other, Vec2) and self.x < other.x and self.y < other.y
    
    def __ge__(self, other):
        return isinstance(other, Vec2) and self.x >= other.x and self.y >= other.y
    
    def __le__(self, other):
        return isinstance(other, Vec2) and self.x <= other.x and self.y <= other.y

    def __iter__(self):
        return iter((self.x, self.y))

    def is_on_edge(self, edge_dir: "Vec2", size: "Vec2") -> bool:
        """
        Returns true iff `self` is on a specific edge of a rectangle with the
        top-left corner at (0, 0), and of the given `size`.
        """
        match edge_dir:
            case Vec2( 1,  0):
                return self.x == size.x-1
            case Vec2( 0,  1):
                return self.y == size.y-1
            case Vec2(-1,  0):
                return self.x == 0
            case Vec2( 0, -1):
                return self.y == 0
            case _:
                raise ValueError("edge_dir must be a cardinal direction")

    __match_args__ = ("x", "y")

CARDINAL_DIRECTIONS = [Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0), Vec2(0, -1)]
