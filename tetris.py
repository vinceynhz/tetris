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
import ansi

from ui import *
from tetromino import *
from math import floor


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

    _move_mapping = {
        'CCW':       lambda f: f.t_current.rotate_ccw(),
        'CW':        lambda f: f.t_current.rotate_cw(), 
        'HARD_DROP': lambda f: f.new_current(),
        'LEFT':      lambda f: f.left_current(),
        'RIGHT':     lambda f: f.right_current()
    }

    def __init__(self):
        self.dim = [ [ '.' for x in range(10) ] for y in range(20) ]

        self.b_board = Box(2, 2, 10, 20)
        self.b_next = Box(2, 30, 4, 4)
        
        self.t_current = None
        self.t_next = None

    def new_current(self):
        self.t_current = Tetromino.rand()
        self.t_current.pos = Coord(
            Tetromino.center(self.b_board.width, self.t_current.width),  # x
            0,                                                          # y
            self.b_board.width - 1 ,                                    # max_x
            self.b_board.height - 1                                     # max_y
        )

    def left_current(self):
        self.t_current.pos -= (1,0)

    def right_current(self):
        self.t_current.pos += (1,0)

    def draw_blocks(self):
        # Draw the main board and whatever elements are there
        ansi.position(self.b_board.pos + (1,1))

        for row in self.dim:
            for cell in row:
                ansi.raw(*Field._dim_mapping[cell])
            ansi.raw(Box.V_LINE)
            ansi.ln(self.b_board.width * 2 + 1) # +1 is for the last character we actually wrote

        # Draw the current tetromino falling
        if self.t_current is not None:
            # Get the current position of the current tetromino
            t_current_pos = self.b_board.pos + self.t_current.pos.map(
                lambda x: 1 + (x * 2),
                lambda y: 1 + y
            )
            ansi.position(t_current_pos)
            self.t_current._print()

        # Draw the next tetromino (aka spare)
        if self.t_next is not None:
            ansi.position(self.b_next.pos + (0, 1))
            self.t_next._print(self.b_next.width)

        ansi.position(1,1)

    def run(self):
        # Here we'll have 2 threads, one counting time and moving the block down
        # and the main one waiting for input
        for c in ansi.read():
            if c == 3: 
                # If Ctrl + C
                break

            with ansi.get_movement(c) as m:
                if m in Field._move_mapping:
                    Field._move_mapping[m](self)
                    self.draw_blocks()

            ansi.clear_line()
            ansi.raw(str(c))

    def start(self):
        # draw the main board
        ansi.clear()

        self.b_board._print()
        self.b_next._print()

        # Add level and score
        ansi.position(30, 9)
        ansi.raw("Level:") 
        ansi.position(30, 10)
        ansi.raw("Score:")

        self.draw_blocks()

        ansi.position(1,1)


    def _push_down(self):
        board_pos = self.b_board.pos + (1,1)
        cur_pos = self.t_current.pos


def main():
    with ansi.Terminal():
        f = Field()
        f.t_next = Tetromino.rand()
        f.new_current()

        f.start()
        f.run()

    ansi.clear()
    # k = Field._color_mapping.keys()
    # for i in range(f.b_board.height):
    #     for j in range(f.b_board.width):
    #         f.dim[i][j] = random.choice(k)


if __name__ == '__main__':
    main()


