"""
    Render mandelbrot on Odroid Go
    It's for loboris MicroPython port!
    
    Based on code from https://github.com/pypyjs/pypyjs-examples/
"""
import sys
import time

import display
import machine
import micropython
from machine import SPI
from micropython import const

micropython.opt_level(99)


def mandelbrot(tft, width, height, left, right, top, bottom, iterations):
    for y in range(height):
        for x in range(width):
            z = complex(0, 0)
            c = complex(left + x * (right - left) / width, top + y * (bottom - top) / height)
            norm = abs(z) ** 2
            for count in range(iterations):
                if norm <= 4:
                    z = z * z + c
                    norm = abs(z * z)
                else:
                    break

            if count <= 4:
                color = tft.DARKGREY
            elif count <= 8:
                color = tft.GREEN
            elif count <= 10:
                color = tft.BLUE
            elif count <= 12:
                color = tft.RED
            elif count <= 15:
                color = tft.YELLOW
            else:
                color = tft.BLACK

            tft.pixel(x, y, color)


def main(screen):
    screen.reset()

    # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/machine#machinewdtenable
    machine.WDT(False)

    start_time = time.time()
    mandelbrot(
        screen,
        width=screen.width,
        height=screen.height,
        left=const(-2),
        right=0.5,
        top=const(1.25),
        bottom=const(-1.25),
        iterations=const(40),
    )
    duration = time.time() - start_time
    print("rendered in %.1f sec." % duration)


if __name__ == "builtins":
    from odroidgo.screen import OdroidGoDisplay

    screen = OdroidGoDisplay()
    main(screen)
    screen.deinit()
    del screen
    print("---END---")
