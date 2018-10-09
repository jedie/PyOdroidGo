"""
    ODROID GO Buttons
"""
import time

import micropython
from machine import ADC, Pin, Timer


class Button:
    """
    Debounced pin handler

    usage e.g.:

    def button_callback(pin):
        print("Button (%s) changed to: %r" % (pin, pin.value()))

    button_handler = Button(pin=Pin(32, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_callback)
    """

    def __init__(
        self,
        pin_no,
        callback,
        min_ago=400,
        mode=Pin.IN,
        pull=Pin.PULL_UP,
        trigger=Pin.IRQ_FALLING,
        debounce=50000,
        acttime=49000,
    ):
        self.callback = callback
        self.min_ago = min_ago

        self._next_call = time.ticks_ms() + self.min_ago

        # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/pin#create-the-pin-instance-object
        self.pin = Pin(
            pin_no,
            mode=mode,
            pull=pull,
            handler=self._irq_handler,
            trigger=trigger,
            debounce=debounce,
            acttime=acttime,
        )

    def _irq_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            # http://docs.micropython.org/en/latest/library/micropython.html#micropython.schedule
            micropython.schedule(self.callback, pin)
        # else:
        #     print("debounce: %s" % (self._next_call - time.ticks_ms()))
