import time

from machine import ADC, Pin, Timer
from micropython import const

BUTTON_MENU = const(13)
BUTTON_VOLUME = const(0)
BUTTON_SELECT = const(27)
BUTTON_START = const(39)

BUTTON_A = const(32)
BUTTON_B = const(33)

# TODO support the crossbar buttons, see:
# https://forum.micropython.org/viewtopic.php?f=2&t=5335
BUTTON_JOY_X = const(34)
BUTTON_JOY_Y = const(35)


class Button:
    """
    Debounced pin handler

    usage e.g.:

    def button_callback(pin):
        print("Button (%s) changed to: %r" % (pin, pin.value()))

    button_handler = Button(pin=Pin(32, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_callback)
    """

    def __init__(self, pin, callback, trigger=Pin.IRQ_FALLING, min_ago=300):
        self.callback = callback
        self.min_ago = min_ago

        self._blocked = False
        self._next_call = time.ticks_ms() + self.min_ago

        pin.irq(trigger=trigger, handler=self.debounce_handler)

    def call_callback(self, pin):
        self.callback(pin)

    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
        # else:
        #     print("debounce: %s" % (self._next_call - time.ticks_ms()))
