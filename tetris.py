import pygame
"""

# To enable colors in windows 10 / this works also for gitbash - need to test in win 8
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# To print a single square
print(u"\u2588\u2588")

# To escape sequences
http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation



"""
def main():
    pygame.init()

    pygame.display.set_caption("mintris")
    screen = pygame.display.set_mode((240, 180))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()


