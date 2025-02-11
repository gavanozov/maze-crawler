#The code is from https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
import os
import sys

class _Getch:
    # Gets a single character from standard input.  Does not echo to the screen
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

if os.path.basename(sys.argv[0]) != "playgame.py":
    script_path = os.path.join(os.path.dirname(__file__), "playgame.py")
    print(f"Wrong file executed! Running '{script_path}' instead...")
    os.system(f'python "{script_path}"')
    sys.exit()