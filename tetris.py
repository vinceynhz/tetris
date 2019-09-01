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

"""
# To print a single square
print(u"\u2588\u2588")
"""

class COLOR:
    RESET = u"\u001b[0m"
    class FG:
        BLACK = u"\u001b[30m"
        RED = u"\u001b[31m"
        GREEN = u"\u001b[32m"
        YELLOW = u"\u001b[33m"
        BLUE = u"\u001b[34m"
        MAGENTA = u"\u001b[35m"
        CYAN = u"\u001b[36m"
        WHITE = u"\u001b[37m"
    class BG:
        LIGHT = ""


class BOX:
    TL_CORNER = u"\u250c"
    TR_CORNER = u"\u2510"
    BL_CORNER = u"\u2514"
    BR_CORNER = u"\u2518"
    H_LINE = u"\u2500"
    V_LINE = u"\u2502"

    def top(size):
        raw(BOX.TL_CORNER)
        for i in range(size): 
            raw(BOX.H_LINE)
        raw(BOX.TR_CORNER)

    def bottom(size):
        raw(BOX.BL_CORNER)
        for i in range(size):
            raw(BOX.H_LINE)
        raw(BOX.BR_CORNER)


BLOCK = u"\u2588\u2588"


class Field:
    def __init__(self):
        self.dim = [ [ '.' for x in range(10) ] for y in range(20) ]

    def print(self):
        clear()

        # First line of the box
        raw("\n ")
        BOX.top(20) # 10 cells * 2 characters for each one
        raw("\n")
        
        for i in range(20):
            raw(" ", BOX.V_LINE)
            for j in range(10):
                cell = self.dim[i][j]
                flag = (j + (i % 2)) % 2 == 0
                if flag: 
                    raw(u"\u001b[38;5;153m")
                raw(BLOCK)
                if flag:
                   raw(COLOR.RESET)
            raw(BOX.V_LINE, "\n")
        
        # Last line of the box
        raw(" ")
        BOX.bottom(20)
        raw("\n")

        # Draw next shape box
        move(30, 2)
        BOX.top(8)

        move(30, 5)
        BOX.bottom(8)

        move(30, 10)
        raw("Level:")

        move(30, 11)
        raw("Score:")


def move(x, y):
    """
    ANSI sequence to move the cursor: 
    CSI y;xf    - move cursor to position y;x 
                - where y represents the line from the top 
                - and x the column from the left
    """
    raw(u"\u001b["+ str(y) + ";" + str(x) + "f")


def clear(x = 1, y = 1):
    """ 
    Call ANSI sequences
    CSI 2J      - erase all screen
    """
    raw(u"\u001b[2J")
    move(x, y)


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

    f = Field()
    f.print()

    # raw(u"\u2588\u2588\u2588\u2588\n\u2588\u2588\u2588\u2588\n\u001b[48;5;239m\u001b[K\n")
    
    time.sleep(2)
    
    # We clear the screen before we finish
    clear()

if __name__ == '__main__':
    main()


