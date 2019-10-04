import random

import ansi
from ui import Color

from math import floor

class Tetromino(object):
    """
    Each of the tetris game pieces are called tetrominos (from the greek prefix tetra = four),
    because each one is composed of four blocks.

    Each shape can be represented by a 4x4 matrix, this matrix will contain every possible shape
    in any of their rotations
    """
    BLOCK = u"\u2588\u2588"

    MAX_POS = None

    color = Color.RESET

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
    def center(in_size, size):
        return int(floor((in_size - size) / 2))

    @staticmethod
    def rand():
        return Tetromino._constructors[random.randint(0,6)]()

    @staticmethod
    def set_max_pos(max_pos):
        Tetromino.MAX_POS = max_pos

    def __init__(self, pos=None, width=4, height=None):
        self.pos = pos # Coord
        self.width = width
        self.height = width if height is None else height
        self.matrix = [ ['.' for col in range(self.width)] for row in range(self.height) ]

    def _print(self, in_size = None):
        if in_size is not None:
            # calculate center in given size
            padding = Tetromino.center(in_size, self.width)
            ansi.move(padding, 'C')
        ansi.raw(self._color())
        for row in self.matrix:
            for col in row:
                if col == '.':
                    ansi.raw('##')
                    # ansi.move(2, 'C')
                else:
                    ansi.raw(Tetromino.BLOCK)
            ansi.ln(self.width * 2)
        ansi.raw(Color.RESET)

    def rotate_cw(self):
        # square matrix rotation
        # new_matrix = [ [ self.matrix[self.size - 1 - x][y] for x in range(self.size) ] for y in range(self.size) ]
        # non square matrix rotation
        self.matrix = [ list(t[::-1]) for t in zip(*self.matrix) ]
        # switch widht and height using tuples
        self.width, self.height = (self.height, self.width)

    def rotate_ccw(self):
        # square matrix rotation
        # new_matrix = [ [ self.matrix[x][self.size - y - 1] for x in range(self.size) ] for y in range(self.size) ]
        # non square matrix rotation
        self.matrix = [ list(t) for t in zip(*self.matrix)][::-1]
        # switch width and height using tuples
        self.width, self.height = (self.height, self.width)

    def left(self):
        if self.pos.x > 0: self.pos.x -= 1

    def right(self):
        if Tetromino.MAX_POS is not None and (self.pos.x + self.width) <= Tetromino.MAX_POS.x: self.pos.x += 1

    def down(self):
        if Tetromino.MAX_POS is not None and (self.pos.y + self.height) <= Tetromino.MAX_POS.y: self.pos.y += 1

    def _color(self):
        return Tetromino.color

class L_Tetromino(Tetromino):
    color = Color.FG.WHITE
    def __init__(self, pos=None):
        Tetromino.__init__(self, pos, 2, 3)
        self.matrix[0][0] = 'L'
        self.matrix[1][0] = 'L'
        self.matrix[2][0] = 'L'
        self.matrix[2][1] = 'L'

    def _color(self):
        return L_Tetromino.color

class J_Tetromino(Tetromino):
    color = Color.FG.BLUE
    def __init__(self, pos=None):
        Tetromino.__init__(self, pos, 2, 3)
        self.matrix[0][1] = 'J'
        self.matrix[1][1] = 'J'
        self.matrix[2][1] = 'J'
        self.matrix[2][0] = 'J'

    def _color(self):
        return J_Tetromino.color

class T_Tetromino(Tetromino):
    color = Color.FG.MAGENTA
    def __init__(self, pos=None):
        Tetromino.__init__(self, pos, 3, 2)
        self.matrix[0][1] = 'T'
        self.matrix[1][0] = 'T'
        self.matrix[1][1] = 'T'
        self.matrix[1][2] = 'T'

    def _color(self):
        return T_Tetromino.color

class O_Tetromino(Tetromino):
    color = Color.FG.YELLOW
    def __init__(self, pos=None):
        Tetromino.__init__(self, pos, 2)
        self.matrix[0][0] = 'O'
        self.matrix[0][1] = 'O'
        self.matrix[1][0] = 'O'
        self.matrix[1][1] = 'O'

    def _color(self):
        return O_Tetromino.color

    def rotate_cw(self):
        pass

    def rotate_ccw(self):
        pass

class S_Tetromino(Tetromino):
    color = Color.FG.GREEN
    def __init__(self, pos=None):
        Tetromino.__init__(self, pos, 3, 2)
        self.matrix[0][1] = 'S'
        self.matrix[0][2] = 'S'
        self.matrix[1][0] = 'S'
        self.matrix[1][1] = 'S'

    def _color(self):
        return S_Tetromino.color

class Z_Tetromino(Tetromino):
    color = Color.FG.RED
    def __init__(self, pos=None):
        Tetromino.__init__(self, pos, 3, 2)
        self.matrix[0][0] = 'Z'
        self.matrix[0][1] = 'Z'
        self.matrix[1][1] = 'Z'
        self.matrix[1][2] = 'Z'

    def _color(self):
        return Z_Tetromino.color

class l_Tetromino(Tetromino):
    color = Color.FG.CYAN
    def __init__(self, pos=None):
        Tetromino.__init__(self, pos, 1, 4)
        self.matrix[0][0] = 'l'
        self.matrix[1][0] = 'l'
        self.matrix[2][0] = 'l'
        self.matrix[3][0] = 'l'

    def _color(self):
        return 
