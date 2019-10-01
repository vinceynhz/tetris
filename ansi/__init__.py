import sys

__win__ = 'win' in sys.platform

if __win__:
    import ctypes
    import msvcrt
else:
    import tty

class Coord(object):
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self):
        return (self.x, self.y)

    def __add__(self, other):
        if type(other) is tuple:
            return (self.x + other[0], self.y + other[1])
        return (self.x + other.x, self.y + other.y)

    def map(self, command_x, command_y):
        return (command_x(self.x), command_y(self.y))

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)


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
    H_LINE = u"\u2500\u2500"
    V_LINE = u"\u2502"
    SPACE = '  '

    pos = None
    width = None
    height = None

    def __init__(self, top, left, width, height):
        """ top and left are relative to the screen """
        self.pos = Coord(left, top)
        self.width = width
        self.height  = height

    def _print(self):
        Screen.position(self.pos())

        Screen.raw(Box.TL_CORNER, Box.H_LINE * self.width, Box.TR_CORNER)
        Screen.ln(self.width * 2 + 2)

        for i in range(self.height):
            Screen.raw(Box.V_LINE, Box.SPACE * self.width, Box.V_LINE)
            Screen.ln(self.width * 2 + 2)

        Screen.raw(Box.BL_CORNER, Box.H_LINE * self.width, Box.BR_CORNER)


class Screen(object):
    _restore = False
    _mode = None
    _arrows_no_win = {
        65: 'UP',
        66: 'DOWN',
        67: 'RIGHT',
        68: 'LEFT'
    }
    _arrows_win = {
        72: 'UP',
        75: 'LEFT',
        77: 'RIGHT',
        80: 'DOWN'
    }
    _arrows = _arrows_win if __win__ else _arrows_no_win
    _arrow_st = 224 if __win__ else 27 

    @staticmethod
    def init():
        if __win__:
            # To enable colors on the console if we're on windows            
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        else:
            try:
                Screen._mode = tty.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin)
                Screen._restore = True
                print(Screen._mode, Screen._restore)
            except tty.error:    # This is the same as termios.error
                print(tty.error)
                sys.exit(-1)

    @staticmethod
    def close():
        if Screen._restore:
            tty.tcsetattr(sys.stdin, tty.TCSAFLUSH, Screen._mode)

    @staticmethod
    def read():
        if __win__:
            return ord(msvcrt.getch())
        else:
            return ord(sys.stdin.read(1))

    @staticmethod
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
        Screen.raw(u"\u001b[{0};{1}f".format(y,x))

    @staticmethod
    def move(n, d):
        """
        n number of positions
        dir direction of the move: (A=up, B=down, C=right, D=left)
        """
        Screen.raw(u"\u001b[{0}{1}".format(n, d))

    @staticmethod
    def ln(n):
        """
        Controlled line jump, to go back n number of characters instead of inserting 0x0D
        """
        Screen.raw(u"\u001b[{0}D\u001b[1B".format(n))

    @staticmethod
    def clear(x = 1, y = 1):
        """ 
        Call ANSI sequence
        CSI 2J      - erase all screen
        """
        Screen.raw(u"\u001b[2J")
        Screen.position(x, y)

    @staticmethod
    def clear_line():
        """
        Call ANSI sequence
        CSI 2K - erase all line
        """
        Screen.raw(u"\u001b[2K")
        Screen.move(1000, 'D')

    @staticmethod
    def is_arrow(n1):
        # If we have the beginning of an arrow
        if n1 == Screen._arrow_st:
            arrow_key = None
            if __win__ or Screen.read() == 91:
                arrow_key = Screen.read()
            if arrow_key is not None and arrow_key in Screen._arrows:
                return Screen._arrows[arrow_key]
        return None

    @staticmethod
    def raw(*args):
        for arg in args:
            if arg is not None:
                sys.stdout.write(arg)
        sys.stdout.flush()
