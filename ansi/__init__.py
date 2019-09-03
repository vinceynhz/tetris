import sys

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

    @staticmethod
    def top(size):
        Screen.raw(Box.TL_CORNER)
        for i in range(size): 
            Screen.raw(Box.H_LINE)
        Screen.raw(Box.TR_CORNER)

    @staticmethod
    def bottom(size):
        Screen.raw(Box.BL_CORNER)
        for i in range(size):
            Screen.raw(Box.H_LINE)
        Screen.raw(Box.BR_CORNER)


class Screen(object):
    @staticmethod
    def move(x, y):
        """
        ANSI sequence to move the cursor: 
        CSI y;xf    - move cursor to position y;x 
                    - where y represents the line from the top 
                    - and x the column from the left
        """
        Screen.raw(u"\u001b["+ str(y) + ";" + str(x) + "f")

    @staticmethod
    def clear(x = 1, y = 1):
        """ 
        Call ANSI sequences
        CSI 2J      - erase all screen
        """
        Screen.raw(u"\u001b[2J")
        Screen.move(x, y)

    @staticmethod
    def raw(*args):
        for arg in args:
            sys.stdout.write(arg)
        sys.stdout.flush()
