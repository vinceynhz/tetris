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
    """ This is to map whichever characters are present in the dim matrix 
        letters represent which type of tetromino there are
    """
        'L': (L_Tetromino.color, Tetromino.BLOCK, Color.RESET),
        'J': (J_Tetromino.color, Tetromino.BLOCK, Color.RESET),
        'T': (T_Tetromino.color, Tetromino.BLOCK, Color.RESET),
        'O': (O_Tetromino.color, Tetromino.BLOCK, Color.RESET),
        'S': (S_Tetromino.color, Tetromino.BLOCK, Color.RESET),
        'Z': (Z_Tetromino.color, Tetromino.BLOCK, Color.RESET),
        'l': (l_Tetromino.color, Tetromino.BLOCK, Color.RESET),
        '.': (Box.SPACE)
    }

    def __init__(self):
        self.dim = [ [ '.' for x in range(10) ] for y in range(20) ]

        self.b_board = Box(2, 2, 10, 20)
        self.b_next = Box(2, 30, 4, 4)
        
        self.t_current = None
        self.t_next = None

    def draw_blocks(self):
        # Draw the main board and whatever elements are there
        Screen.position(self.b_board.pos + (1,1))

        for row in self.dim:
            for cell in row:
                Screen.raw(*Field._dim_mapping[cell])
            Screen.raw(Box.V_LINE)
            Screen.ln(self.b_board.width * 2 + 1) # +1 is for the last character we actually wrote

        # Draw the current tetromino falling
        if self.t_current is not None:
            # Get the current position of the current tetromino
            t_current_pos = self.b_board.pos + self.t_current.pos.map(
                lambda x: 1 + (x * 2),
                lambda y: 1 + y
            )
            Screen.position(t_current_pos)
            self.t_current._print()

        # Draw the next tetromino (aka spare)
        if self.t_next is not None:
            Screen.position(self.b_next.pos + (0, 1))
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
                    self.t_current.pos = Coord(Tetromino.center(self.b_board.width, self.t_current.size), 0)

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
        board_pos = self.b_board.pos + (1,1)
        cur_pos = self.t_current.pos


def main():
    Screen.init()

    f = Field()

    f.t_next = Tetromino.rand()
    f.t_current = Tetromino.rand()
    f.t_current.pos = Coord(Tetromino.center(f.b_board.width, f.t_current.size), 0)

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

if __name__ == '__main__':
    main()


