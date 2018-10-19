import sys

from odroidgo.screen import screen


def main():
    print("sys.exit()")
    screen.print("sys.exit()")
    sys.exit()


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
