import ansi

class Coord(object):
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self):
        return (self.x, self.y)

    def __add__(self, other):
        ax, ay = self._other(other)
        return (self.x + ax, self.y + ay)

    def __iadd__(self, other):
        self.x, self.y = self.__add__(other)
        return self

    def __sub__(self, other):
        ax, ay = self._other(other)
        return (self.x + ax, self.y + ay)
        
    def __isub__(self, other):
        self.x, self.y = self.__sub__(other)
        return self

    def map(self, command_x, command_y):
        return (command_x(self.x), command_y(self.y))

    def _other(self, other):
        if type(other) is tuple:
            return other
        else:
            return other.x, other.y

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)


class Color(object):
    RESET = u"\u001b[0m"

    class FG(object):
        BLACK = u"\u001b[30m"
        RED = u"\u001b[31m"
        GREEN = u"\u001b[32m"
        YELLOW = u"\u001b[33m"
        BLUE = u"\u001b[34m"
        MAGENTA = u"\u001b[35m"
        CYAN = u"\u001b[36m"
        WHITE = u"\u001b[37m"

    class BG(object):
        LIGHT = ""


class Box(object):
    TL_CORNER = u"\u250c"
    TR_CORNER = u"\u2510"
    BL_CORNER = u"\u2514"
    BR_CORNER = u"\u2518"
    H_LINE = u"\u2500\u2500"
    V_LINE = u"\u2502"
    SPACE = '  '

    pos = None
    width = None
    height = None

    def __init__(self, top, left, width, height):
        """ top and left are relative to the screen """
        self.pos = Coord(left, top)
        self.width = width
        self.height  = height

    def _print(self):
        ansi.position(self.pos())

        ansi.raw(Box.TL_CORNER, Box.H_LINE * self.width, Box.TR_CORNER)
        ansi.ln(self.width * 2 + 2)

        for i in range(self.height):
            ansi.raw(Box.V_LINE, Box.SPACE * self.width, Box.V_LINE)
            ansi.ln(self.width * 2 + 2)

        ansi.raw(Box.BL_CORNER, Box.H_LINE * self.width, Box.BR_CORNER)
