import random

from ansi import Screen, Color

from math import floor



class Tetromino(object):
    """
    Each of the tetris game pieces are called tetrominos (from the greek prefix tetra = four),
    because each one is composed of four blocks.

    Each shape can be represented by a 4x4 matrix, this matrix will contain every possible shape
    in any of their rotations
    """
    BLOCK = u"\u2588\u2588"

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

    def __init__(self, size=4):
        self.pos = None
        self.size = size
        self.matrix = [ ['.' for x in range(size)] for y in range(size) ]

    def _print(self, in_size = None):
        if in_size is not None:
            # calculate center in given size
            padding = Tetromino.center(in_size, self.size)
            Screen.move(padding, 'C')
        Screen.raw(self._color())
        for row in self.matrix:
            for col in row:
                if col == '.':
                    Screen.move(2, 'C')
                else:
                    Screen.raw(Tetromino.BLOCK)
            Screen.ln(self.size * 2)
        Screen.raw(Color.RESET)

    def rotate_cw(self):
        new_matrix = [ [ self.matrix[self.size - 1 - x][y] for x in range(self.size) ] for y in range(self.size) ]
        self.matrix = new_matrix

    def rotate_ccw(self):
        new_matrix = [ [ self.matrix[x][self.size - y - 1] for x in range(self.size) ] for y in range(self.size) ]
        self.matrix = new_matrix

    def _color(self):
        return Tetromino.color

class L_Tetromino(Tetromino):
    color = Color.FG.WHITE
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][1] = 'L'
        self.matrix[1][1] = 'L'
        self.matrix[2][1] = 'L'
        self.matrix[2][2] = 'L'

    def _color(self):
        return L_Tetromino.color


class J_Tetromino(Tetromino):
    color = Color.FG.BLUE
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][1] = 'J'
        self.matrix[1][1] = 'J'
        self.matrix[2][1] = 'J'
        self.matrix[2][0] = 'J'

    def _color(self):
        return J_Tetromino.color

class T_Tetromino(Tetromino):
    color = Color.FG.MAGENTA
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][1] = 'T'
        self.matrix[1][0] = 'T'
        self.matrix[1][1] = 'T'
        self.matrix[1][2] = 'T'

    def _color(self):
        return T_Tetromino.color


class O_Tetromino(Tetromino):
    color = Color.FG.YELLOW
    def __init__(self):
        Tetromino.__init__(self, 2)
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
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][1] = 'S'
        self.matrix[0][2] = 'S'
        self.matrix[1][0] = 'S'
        self.matrix[1][1] = 'S'

    def _color(self):
        return S_Tetromino.color


class Z_Tetromino(Tetromino):
    color = Color.FG.RED
    def __init__(self):
        Tetromino.__init__(self, 3)
        self.matrix[0][0] = 'Z'
        self.matrix[0][1] = 'Z'
        self.matrix[1][1] = 'Z'
        self.matrix[1][2] = 'Z'

    def _color(self):
        return Z_Tetromino.color


class l_Tetromino(Tetromino):
    color = Color.FG.CYAN
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][1] = 'l'
        self.matrix[1][1] = 'l'
        self.matrix[2][1] = 'l'
        self.matrix[3][1] = 'l'

    def _color(self):
        return 
