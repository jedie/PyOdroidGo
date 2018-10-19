"""
    Odroid Go crossbar test
"""

from odroidgo.crossbar import Crossbar
from odroidgo.screen import screen


class CrossbarPrintHandler:
    def up(self):
        screen.print("up")

    def down(self):
        screen.print("down")

    def right(self):
        screen.print("right")

    def left(self):
        screen.print("left")


def main():
    crossbar_handler = CrossbarPrintHandler()
    crossbar = Crossbar(crossbar_handler)
    screen.print("poll loop started...")
    while True:
        crossbar.poll()


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
