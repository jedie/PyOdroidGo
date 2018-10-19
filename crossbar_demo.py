"""
    Odroid Go crossbar test
"""

from odroidgo.crossbar import Crossbar


class CrossbarPrintHandler:
    def __init__(self, screen):
        self.screen = screen

    def up(self):
        self.screen.print("up")

    def down(self):
        self.screen.print("down")

    def right(self):
        self.screen.print("right")

    def left(self):
        self.screen.print("left")


def main(screen):
    crossbar_handler = CrossbarPrintHandler(screen)
    crossbar = Crossbar(crossbar_handler)
    screen.print("poll loop started...")
    while True:
        crossbar.poll()


if __name__ == "builtins":
    from odroidgo.screen import OdroidGoDisplay

    screen = OdroidGoDisplay()
    main(screen)
