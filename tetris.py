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

class FG:
    BLACK = u"\u001b[30m"
    RED = u"\u001b[31m"
    GREEN = u"\u001b[32m"
    YELLOW = u"\u001b[33m"
    BLUE = u"\u001b[34m"
    MAGENTA = u"\u001b[35m"
    CYAN = u"\u001b[36m"
    WHITE = u"\u001b[37m"
    RESET = u"\u001b[0m"

class BG:
    LIGHT = ""    

class Field:
    def __init__(self):
        self.dim = [ [ '.' for x in range(10) ] for y in range(20) ]

    def print(self):
        raw(u"\n \u250c")
        for i in range(20): # 10 cells * 2 characters for each one
            raw(u"\u2500")
        raw(u"\u2510\n")
        for i in range(20):
            raw(u" \u2502")
            for j in range(10):
                cell = self.dim[i][j]
                flag = (j + (i % 2)) % 2 == 0
                if flag: 
                    raw(u"\u001b[38;5;153m")
                raw(u"\u2588\u2588")
                if flag:
                   raw(u"\u001b[0m")
            raw(u"\u2502\n")
        raw(u" \u2514")
        for i in range(20):
            raw(u"\u2500")
        raw(u"\u2518\n")

def clear():
    """ 
    Call ANSI sequences
    CSI 2J      - erase all screen
    CSI 1;1f    - move cursor to top left
    """
    raw(u"\u001b[2J\u001b[1;1f")

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

    # We start by clearing the screen
    clear()
    # raw(u"\u001b[48;5;239m\u001b[K");

    f = Field()
    f.print()

    # raw(u"\u2588\u2588\u2588\u2588\n\u2588\u2588\u2588\u2588\n\u001b[48;5;239m\u001b[K\n")
    
    # raw(u"\u001b[0m")
    time.sleep(2)
    
    # We clear the screen before we finish
    clear()

if __name__ == '__main__':
    main()


