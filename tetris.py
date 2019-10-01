"""
Tetris game for the terminal using ANSI Escape Sequences.

Documentation and reference about Escape Sequences used for this game:

- http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation
- http://courseweb.stthomas.edu/tpsturm/private/notes/qm300/ANSI.html

Documentation of some printable special characters:

- https://www.w3schools.com/charsets/ref_utf_box.asp

Rx Py (for python 3.6 and above):

- https://github.com/ReactiveX/RxPY

"""
import threading
import time

from math import floor

from tetromino import *
from ansi import *


class Field(object):
    _dim_mapping = {
        'L': (Color.FG.WHITE, Tetromino.BLOCK, Color.RESET),
        'J': (Color.FG.BLUE, Tetromino.BLOCK, Color.RESET),
        'T': (Color.FG.MAGENTA, Tetromino.BLOCK, Color.RESET),
        'O': (Color.FG.YELLOW, Tetromino.BLOCK, Color.RESET),
        'S': (Color.FG.RED, Tetromino.BLOCK, Color.RESET),
        'Z': (Color.FG.GREEN, Tetromino.BLOCK, Color.RESET),
        'l': (Color.FG.CYAN, Tetromino.BLOCK, Color.RESET),
        '.': ('  ')
    }


    def __init__(self):
        self.dim = [ [ '.' for x in range(10) ] for y in range(20) ]
        self.b_board = Box(2, 2, 10, 20)
        self.b_next = Box(2, 30, 4, 4)
        
        self.t_current = None
        self.t_next = None

    def draw_blocks(self):
        # Draw the main board and whatever elements are there
        Screen.position(self.b_board.left + 1, self.b_board.top + 1)

        for row in self.dim:
            for cell in row:
                Screen.raw(*Field._dim_mapping[cell])
            Screen.raw(Box.V_LINE)
            Screen.ln(self.b_board.width * 2 + 1) # +1 is for the last character we actually wrote

        # Draw the current tetromino falling
        if self.t_current is not None:
            Screen.position(
                self.b_board.left + 1 + (self.t_current.pos[0] * 2),
                self.b_board.top + self.t_current.pos[1] + 1,
            )
            self.t_current._print()

        # Draw the next tetromino (aka spare)
        if self.t_next is not None:
            Screen.position(
                self.b_next.left, 
                self.b_next.top + 1
            )
            self.t_next._print(self.b_next.width)

        Screen.position(1,1)

    def run(self):
        # Here we'll have 2 threads, one counting time and moving the block down
        # and the main one waiting for input
        while True:
            c = Screen.read() # Read one char from the stdinput
            
            if c == 3: # This corresponds to Ctrl + C
                break 

            a = Screen.is_arrow(c)
            if a is not None:
                if a == 'LEFT':
                    self.t_current.rotate_ccw()
                elif a == 'RIGHT':
                    self.t_current.rotate_cw()
                elif a == 'UP':
                    self.t_current = Tetromino.rand()
                    self.t_current.pos = (Tetromino.center(self.b_board.width, self.t_current.size), 0)

                self.draw_blocks()

            Screen.clear_line()
            Screen.raw(str(c))

    def start(self):
        # draw the main board
        Screen.clear()

        self.b_board._print()
        self.b_next._print()

        # Add level and score
        Screen.position(30, 9)
        Screen.raw("Level:")

        Screen.position(30, 10)
        Screen.raw("Score:")

        self.draw_blocks()

        Screen.position(1,1)

    def _push_down(self):
        pass
            

def main():
    Screen.init()

    f = Field()

    f.t_next = Tetromino.rand()
    f.t_current = Tetromino.rand()
    f.t_current.pos = (Tetromino.center(f.b_board.width, f.t_current.size), 0)
    print f.t_current.pos

    # k = Field._color_mapping.keys()
    # for i in range(f.b_board.height):
    #     for j in range(f.b_board.width):
    #         f.dim[i][j] = random.choice(k)

    try:
        f.start()
        f.run()
    finally:
        Screen.close()
        Screen.clear()
    # Tetromino.rand()._print()

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

if __name__ == '__main__':
    main()


