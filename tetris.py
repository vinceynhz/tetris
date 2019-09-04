"""
Tetris game for the terminal using ANSI Escape Sequences.

Documentation and reference about Escape Sequences used for this game:

- http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation
- http://courseweb.stthomas.edu/tpsturm/private/notes/qm300/ANSI.html

Documentation of some printable special characters:

- https://www.w3schools.com/charsets/ref_utf_box.asp

In python 2.7 we can't have a print method

"""
import sys
import time

from tetromino import *
from ansi import *

class Field(object):
    _color_mapping = {
        'L': Color.FG.WHITE,
        'J': Color.FG.BLUE,
        'T': Color.FG.MAGENTA,
        'O': Color.FG.YELLOW,
        'S': Color.FG.RED,
        'Z': Color.FG.GREEN,
        'l': Color.FG.CYAN
    }

    def __init__(self):
        self.dim = [ [ '.' for x in range(10) ] for y in range(20) ]


    def _print(self):
        Screen.clear()

        # First line of the box
        Screen.raw("\n ")
        Box.top(20) # 10 cells * 2 characters for each one
        Screen.raw("\n")
        
        for i in range(20):
            Screen.raw(" ", Box.V_LINE)
            for j in range(10):
                cell = self.dim[i][j]
                if cell == '.': 
                    Screen.raw('  ')
                else:
                    Screen.raw(Field._color_mapping[cell], Tetromino.BLOCK)
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


def main():
    if 'win' in sys.platform:
        # To enable colors on the console if we're on windows
        import ctypes
        
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    f = Field()
    f._print()

    #l = L_Tetromino()
    #l._print()
    # Screen.raw('\n')

    # l.rotate_cw()
    # l.print()
    # l.rotate_cw()
    # l.print()
    # l.rotate_cw()
    # l.print()
    # l.rotate_cw()
    # l.print() # back to the original position

    # Screen.raw('\n')
    
    # l.rotate_ccw()
    # l.print()
    # l.rotate_ccw()
    # l.print()
    # l.rotate_ccw()
    # l.print()
    # l.rotate_ccw()
    # l.print() # back to the original position

    # j = J_Tetromino()
    # j.print()

    # t = T_Tetromino()
    # t.print()

    # o = O_Tetromino()
    # o.print()

    # s = S_Tetromino()
    # s.print()

    # z = Z_Tetromino()
    # z.print()

    # i = l_Tetromino()
    # i.print()


    # raw(u"\u2588\u2588\u2588\u2588\n\u2588\u2588\u2588\u2588\n\u001b[48;5;239m\u001b[K\n")
    
    time.sleep(2)
    
    # We clear the screen before we finish
    Screen.clear()

if __name__ == '__main__':
    main()


