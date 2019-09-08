"""
Tetris game for the terminal using ANSI Escape Sequences.

Documentation and reference about Escape Sequences used for this game:

- http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation
- http://courseweb.stthomas.edu/tpsturm/private/notes/qm300/ANSI.html

Documentation of some printable special characters:

- https://www.w3schools.com/charsets/ref_utf_box.asp

In python 2.7 we can't have a print method

"""
import threading
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
        self.b_board = Box(2, 2, 10, 20)
        self.b_next = Box(2, 30, 4, 4)
        
        self.t_current = None
        self.t_next = None

    def draw_blocks(self):
        Screen.position(self.b_board.left + 1, self.b_board.top + 1)
        for i in range(self.b_board.height):
            for j in range(self.b_board.width):
                cell = self.dim[i][j]
                if cell == '.': 
                    Screen.move(2, 'C')
                else:
                    Screen.raw(Field._color_mapping[cell], Tetromino.BLOCK)
                    Screen.raw(Color.RESET)
            Screen.raw(Box.V_LINE)
            Screen.ln(self.b_board.width * 2 + 1) # +1 is for the last character we actually wrote

    def start(self):
        # draw the main board
        Screen.clear()

        self.b_board._print()
        self.b_next._print()

        Screen.position(30, 9)
        Screen.raw("Level:")

        Screen.position(30, 10)
        Screen.raw("Score:")

        self.draw_blocks()

        if self.t_next is not None:
            Screen.position(self.b_next.left + 1, self.b_next.top + 1)
            self.t_next._print(self.b_next.width)


        Screen.position(1,1)

        # Here we'll have 2 threads, one counting time and moving the block down
        # and the main one waiting for input
        while True:
            c = Screen.read() # Read one char from the stdinput
            
            if c == 3: # This corresponds to Ctrl + C
                break 

            Screen.raw("New char", chr(c))
            

def main():
    Screen.init()

    f = Field()

    f.t_next = Tetromino.rand()
    f.t_current = Tetromino.rand()
    f.t_current.pos = 

    # k = Field._color_mapping.keys()
    # for i in range(f.b_board.height):
    #     for j in range(f.b_board.width):
    #         f.dim[i][j] = random.choice(k)

    f.start()
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


    # raw(u"\u2588\u2588\u2588\u2588\n\u2588\u2588\u2588\u2588\n\u001b[48;5;239m\u001b[K\n")
    
    Screen.close()
    # We clear the screen before we finish
    Screen.clear()

if __name__ == '__main__':
    main()


