"""
Tetris game for the terminal using ANSI Escape Sequences.

Documentation and reference about Escape Sequences used for this game:

- http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation
- http://courseweb.stthomas.edu/tpsturm/private/notes/qm300/ANSI.html

Documentation of some printable special characters:

- https://www.w3schools.com/charsets/ref_utf_box.asp

"""
from __future__ import print_function

import sys
import time

class Tetromino(object):
    """
    Each of the tetris game pieces are called tetrominos (from the greek prefix tetra = four),
    because each one is composed of four blocks.

    Each shape can be represented by a 4x4 matrix, this matrix will contain every possible shape
    in any of their rotations
    """
    BLOCK = u"\u2588\u2588"

    def __init__(self):
        self.pos = None
        self.matrix = [ ['.' for x in range(4)] for y in range(4) ]

    def print(self):
        Screen.raw(self._color())
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == '.':
                    Screen.raw('  ')
                else:
                    Screen.raw(Tetromino.BLOCK)
            Screen.raw('\n')
        Screen.raw(Color.RESET)

    def _color(self):
        return Color.RESET

    def rotate_cw(self):
        pass

    def rotate_ccw(self):
        pass


class L_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][0] = 'x'
        self.matrix[1][0] = 'x'
        self.matrix[2][0] = 'x'
        self.matrix[2][1] = 'x'

    def _color(self):
        return Color.FG.WHITE


class J_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][1] = 'x'
        self.matrix[1][1] = 'x'
        self.matrix[2][1] = 'x'
        self.matrix[2][0] = 'x'

    def _color(self):
        return Color.FG.BLUE


class T_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][0] = 'x'
        self.matrix[0][1] = 'x'
        self.matrix[0][2] = 'x'
        self.matrix[1][1] = 'x'

    def _color(self):
        return Color.FG.MAGENTA


class O_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][0] = 'x'
        self.matrix[0][1] = 'x'
        self.matrix[1][0] = 'x'
        self.matrix[1][1] = 'x'

    def _color(self):
        return Color.FG.YELLOW


class S_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][1] = 'x'
        self.matrix[0][2] = 'x'
        self.matrix[1][0] = 'x'
        self.matrix[1][1] = 'x'

    def _color(self):
        return Color.FG.GREEN


class Z_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][0] = 'x'
        self.matrix[0][1] = 'x'
        self.matrix[1][1] = 'x'
        self.matrix[1][2] = 'x'

    def _color(self):
        return Color.FG.RED


class l_Tetromino(Tetromino):
    def __init__(self):
        Tetromino.__init__(self)
        self.matrix[0][0] = 'x'
        self.matrix[1][0] = 'x'
        self.matrix[2][0] = 'x'
        self.matrix[3][0] = 'x'

    def _color(self):
        return Color.FG.CYAN


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
    H_LINE = u"\u2500"
    V_LINE = u"\u2502"

    @staticmethod
    def top(size):
        Screen.raw(Box.TL_CORNER)
        for i in range(size): 
            Screen.raw(Box.H_LINE)
        Screen.raw(Box.TR_CORNER)

    @staticmethod
    def bottom(size):
        Screen.raw(Box.BL_CORNER)
        for i in range(size):
            Screen.raw(Box.H_LINE)
        Screen.raw(Box.BR_CORNER)


class Field(object):
    def __init__(self):
        self.dim = [ [ '.' for x in range(10) ] for y in range(20) ]

    def print(self):
        Screen.clear()

        # First line of the box
        Screen.raw("\n ")
        Box.top(20) # 10 cells * 2 characters for each one
        Screen.raw("\n")
        
        for i in range(20):
            Screen.raw(" ", Box.V_LINE)
            for j in range(10):
                cell = self.dim[i][j]
                flag = (j + (i % 2)) % 2 == 0
                if flag: 
                    Screen.raw(u"\u001b[38;5;153m")
                Screen.raw(Tetromino.BLOCK)
                if flag:
                   Screen.raw(Color.RESET)
            Screen.raw(Box.V_LINE, "\n")
        
        # Last line of the Box
        Screen.raw(" ")
        Box.bottom(20)
        Screen.raw("\n")

        # Draw next shape Box
        Screen.move(30, 2)
        Box.top(8)

        Screen.move(30, 5)
        Box.bottom(8)

        Screen.move(30, 10)
        Screen.raw("Level:")

        Screen.move(30, 11)
        Screen.raw("Score:")


class Screen(object):
    @staticmethod
    def move(x, y):
        """
        ANSI sequence to move the cursor: 
        CSI y;xf    - move cursor to position y;x 
                    - where y represents the line from the top 
                    - and x the column from the left
        """
        Screen.raw(u"\u001b["+ str(y) + ";" + str(x) + "f")

    @staticmethod
    def clear(x = 1, y = 1):
        """ 
        Call ANSI sequences
        CSI 2J      - erase all screen
        """
        Screen.raw(u"\u001b[2J")
        Screen.move(x, y)

    @staticmethod
    def raw(*args):
        for arg in args:
            sys.stdout.write(arg)
        sys.stdout.flush()


def main():
    if 'win' in sys.platform:
        # To enable colors on the console if we're on windows
        import ctypes
        
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    # f = Field()
    # f.print()

    l = L_Tetromino()
    l.print()

    j = J_Tetromino()
    j.print()

    t = T_Tetromino()
    t.print()

    o = O_Tetromino()
    o.print()

    s = S_Tetromino()
    s.print()

    z = Z_Tetromino()
    z.print()

    i = l_Tetromino()
    i.print()


    # raw(u"\u2588\u2588\u2588\u2588\n\u2588\u2588\u2588\u2588\n\u001b[48;5;239m\u001b[K\n")
    
    time.sleep(2)
    
    # We clear the screen before we finish
    Screen.clear()

if __name__ == '__main__':
    main()


