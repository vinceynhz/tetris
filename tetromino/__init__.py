import random

from ansi import Screen, Color

class Tetromino(object):
    """
    Each of the tetris game pieces are called tetrominos (from the greek prefix tetra = four),
    because each one is composed of four blocks.

    Each shape can be represented by a 4x4 matrix, this matrix will contain every possible shape
    in any of their rotations
    """
    BLOCK = u"\u2588\u2588"

    _constructors = [
        lambda: L_Tetromino(),
        lambda: J_Tetromino(),
        lambda: T_Tetromino(),
        lambda: O_Tetromino(),
        lambda: S_Tetromino(),
        lambda: Z_Tetromino(),
        lambda: l_Tetromino()
    ]

    @staticmethod
    def rand():
        return Tetromino._constructors[random.randint(0,6)]()

    def __init__(self, size=4):
        self.pos = None
        self.size = size
        self.matrix = [ ['.' for x in range(size)] for y in range(size) ]

    def _print(self):
        Screen.raw(self._color())
        for y in range(self.size):
            for x in range(self.size):
                if self.matrix[y][x] == '.':
                    Screen.raw('  ')
                else:
                    Screen.raw(Tetromino.BLOCK)
            Screen.ln(self.size * 2)
        Screen.raw(Color.RESET)

    def _color(self):
        return Color.RESET

    def rotate_cw(self):
        new_matrix = [ [ self.matrix[self.size - 1 - x][y] for x in range(self.size) ] for y in range(self.size) ]
        self.matrix = new_matrix

    def rotate_ccw(self):
        new_matrix = [ [ self.matrix[x][self.size - y - 1] for x in range(self.size) ] for y in range(self.size) ]
        self.matrix = new_matrix


class L_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][1] = 'L'
        self.matrix[1][1] = 'L'
        self.matrix[2][1] = 'L'
        self.matrix[2][2] = 'L'

    def _color(self):
        return Color.FG.WHITE


class J_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][1] = 'J'
        self.matrix[1][1] = 'J'
        self.matrix[2][1] = 'J'
        self.matrix[2][0] = 'J'

    def _color(self):
        return Color.FG.BLUE


class T_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[1][0] = 'T'
        self.matrix[1][1] = 'T'
        self.matrix[1][2] = 'T'
        self.matrix[2][1] = 'T'

    def _color(self):
        return Color.FG.MAGENTA


class O_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self, 2)
        self.matrix[0][0] = 'x'
        self.matrix[0][1] = 'x'
        self.matrix[1][0] = 'x'
        self.matrix[1][1] = 'x'

    def _color(self):
        return Color.FG.YELLOW


class S_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][1] = 'x'
        self.matrix[0][2] = 'x'
        self.matrix[1][0] = 'x'
        self.matrix[1][1] = 'x'

    def _color(self):
        return Color.FG.GREEN


class Z_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][0] = 'x'
        self.matrix[0][1] = 'x'
        self.matrix[1][1] = 'x'
        self.matrix[1][2] = 'x'

    def _color(self):
        return Color.FG.RED


class l_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][1] = 'x'
        self.matrix[1][1] = 'x'
        self.matrix[2][1] = 'x'
        self.matrix[3][1] = 'x'

    def _color(self):
        return Color.FG.CYAN
