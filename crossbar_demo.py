import time

from odroidgo.crossbar import Crossbar


class CrossbarHandler:
    def __init__(self, print_func):
        self.print_func = print_func

    def up(self):
        self.print_func("up")

    def down(self):
        self.print_func("down")

    def right(self):
        self.print_func("right")

    def left(self):
        self.print_func("left")


def main(lcd, print_func):
    crossbar_handler = CrossbarHandler(print_func)
    crossbar = Crossbar(crossbar_handler)

    print_func("poll loop started...")

    for i in range(100):
        crossbar.poll()
        time.sleep(0.1)

    print_func("--END--")
