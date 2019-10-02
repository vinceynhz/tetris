import sys
from contextlib import contextmanager 

__win__ = 'win' in sys.platform

if __win__:
    import ctypes
    import msvcrt
else:
    import tty

_arrow_st = 224 if __win__ else 27 
# Keyboard letters to move/rotate tetrominoes
_key_move = {
    # lowercase      # uppercase
    97:  'CCW',      65: 'CCW',      # aA
    100: 'CW',       68: 'CW',       # dD
    105: 'HARD_DROP',73: 'HARD_DROP',# iI
    106: 'LEFT',     74: 'LEFT',     # jJ
    108: 'RIGHT',    76: 'RIGHT',    # lL
    107: 'DOWN',     75: 'DOWN'      # kK
}
# Actual keyboard arrows
_arrows = {
    # linux          # windows
    72: 'HARD_DROP', 65: 'HARD_DROP',
    75: 'LEFT',      68: 'LEFT',
    77: 'RIGHT',     67: 'RIGHT',
    80: 'DOWN',      66: 'DOWN'
}

class Terminal(object):
    def __init__(self):
        self.mode = None
        self.restore = False

    def __enter__(self):
        if __win__:
            # To enable colors on the console if we're on windows            
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        else:
            try:
                self.mode = tty.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin)
                self.restore = True
                print(self.mode, self.restore)
            except tty.error:    # This is the same as termios.error
                print(tty.error)
                sys.exit(-1)

    def __exit__(self, *args):
        """ in python 2.7, the __exit__ method receives other parameters besides self """
        if self.restore:
            tty.tcsetattr(sys.stdin, tty.TCSAFLUSH, self.mode)

def read():
    """ Generator of characters read from keyboard """
    while True:
        yield _single_read()

def _single_read():
    if __win__:
        i = msvcrt.getch()
    else:
        i = sys.stdin.read(1)
    return ord(i)

def position(x, y = None):
    """
    ANSI sequence to position the cursor: 
    CSI y;xf    - move cursor to position y;x 
                - where y represents the line from the top 
                - and x the column from the left
    """
    if type(x) is tuple:
        y = x[1]
        x = x[0]
    raw(u"\u001b[{0};{1}f".format(y,x))

def move(n, d):
    """
    n number of positions
    dir direction of the move: (A=up, B=down, C=right, D=left)
    """
    raw(u"\u001b[{0}{1}".format(n, d))

def ln(n):
    """
    Controlled line jump, to go back n number of characters instead of inserting 0x0D
    """
    raw(u"\u001b[{0}D\u001b[1B".format(n))

def clear(x = 1, y = 1):
    """ 
    Call ANSI sequence
    CSI 2J      - erase all screen
    """
    raw(u"\u001b[2J")
    position(x, y)

def clear_line():
    """
    Call ANSI sequence
    CSI 2K - erase all line
    """
    raw(u"\u001b[2K")
    move(1000, 'D')

@contextmanager
def get_movement(n1):
    res = None
    # If we have ADIJKL case insensitive
    if n1 in _key_move:
        res = _key_move[n1]
    # If we have the beginning of an arrow
    elif n1 == _arrow_st:
        arrow_key = None
        if __win__ or _single_read() == 91:
            arrow_key = _single_read()
        if arrow_key in _arrows:
            res = _arrows[arrow_key]
    yield res

def raw(*args):
    for arg in args:
        if arg is not None:
            sys.stdout.write(arg)
    sys.stdout.flush()

