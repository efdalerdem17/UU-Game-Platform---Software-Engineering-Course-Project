from .color import Color, print_color


class Stone:
    def __init__(self, color: Color, is_standing: bool):
        self.color = color
        self.is_standing = is_standing

    def __str__(self):
        return f"Stone({print_color(self.color)}, {'S' if self.is_standing else 'F'})"

    def __repr__(self):
        return self.__str__()
