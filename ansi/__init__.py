import sys

__win__ = 'win' in sys.platform

if __win__:
    import ctypes
    import msvcrt
else:
    import tty

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

    top = None
    left = None
    width = None
    height = None

    def __init__(self, top, left, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height  = height

    def _print(self):
        Screen.position(self.left, self.top)

        Screen.raw(Box.TL_CORNER)
        for i in range(self.width * 2): 
            Screen.raw(Box.H_LINE)
        Screen.raw(Box.TR_CORNER)
        Screen.ln(self.width * 2 + 2)

        for i in range(self.height):
            Screen.raw(Box.V_LINE)
            for j in range(self.width):
                Screen.raw('  ')
            Screen.raw(Box.V_LINE)
            Screen.ln(self.width * 2 + 2)

        Screen.raw(Box.BL_CORNER)
        for i in range(self.width * 2):
            Screen.raw(Box.H_LINE)
        Screen.raw(Box.BR_CORNER)

class Screen(object):
    _restore = False
    _mode = None
    _arrows = {
        65: 'UP',
        66: 'DOWN',
        67: 'RIGHT',
        68: 'LEFT'
    }

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
    def position(x, y):
        """
        ANSI sequence to position the cursor: 
        CSI y;xf    - move cursor to position y;x 
                    - where y represents the line from the top 
                    - and x the column from the left
        """
        Screen.raw(u"\u001b["+ str(y) + ";" + str(x) + "f")

    @staticmethod
    def move(n, dir):
        """
        n number of positions
        dir direction of the move: (A=up, B=down, C=right, D=left)
        """
        Screen.raw(u"\u001b[" + str(n) + dir)

    @staticmethod
    def ln(n):
        """
        Controlled line jump, to go back n number of characters instead of inserting 0x0D
        """
        Screen.raw(u"\u001b[" + str(n) + 'D', u"\u001b[1B")

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
        if n1 == 27:
            # we read next two
            n2, n3 = Screen.read(), Screen.read()
            if n2 == 91 and n3 in Screen._arrows:
                return Screen._arrows[n3]
        return None

    @staticmethod
    def raw(*args):
        for arg in args:
            sys.stdout.write(arg)
        sys.stdout.flush()
