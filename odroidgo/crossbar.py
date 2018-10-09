"""
    ODROID GO Crossbar

    release value = 142

    joy-x button adc values: left 2500 - right 1200
    joy-y button adc values: up 2500 - down 1200
"""
import sys
import time

import machine
import odroidgo
from machine import ADC, Pin, Timer


class JoystickHandler:
    def __init__(self, pin_no, high_callback, low_callback):
        # set PULL_UP will raise into:
        # ValueError: pins 34~39 do not have pull-up or pull-down circuitry
        pin = Pin(pin_no, mode=Pin.IN)  # , pull=Pin.PULL_UP)

        self.high_callback = high_callback
        self.low_callback = low_callback

        try:
            self.adc = ADC(pin)
        except OSError as err:
            # e.g.: ValueError: pin already used for adc
            sys.print_exception(err)
            for i in range(3, 0, -1):
                print("Hard reset in %i Sek!" % i)
                time.sleep(1)
            machine.reset()

        self.adc.width(ADC.WIDTH_9BIT)
        self.adc.atten(ADC.ATTN_11DB)

        self.blocked = False

    def poll(self):
        value = self.adc.read()
        if value < odroidgo.BUTTON_JOY_MIN_ADC:
            # button released
            self.blocked = False
        elif not self.blocked:
            if value > odroidgo.BUTTON_JOY_MIN_ADC_HIGH:
                self.blocked = True
                self.high_callback()
            elif value > odroidgo.BUTTON_JOY_MIN_ADC_LOW:
                self.blocked = True
                self.low_callback()


class Crossbar:
    """
    usage example:

        crossbar_handler = CrossbarPrintHandler()
        crossbar = Crossbar(crossbar_handler)
        print("poll loop started...")
        while True:
            crossbar.poll()
    """

    def __init__(self, handler):
        self.joy_x = JoystickHandler(odroidgo.BUTTON_JOY_X, high_callback=handler.left, low_callback=handler.right)
        self.joy_y = JoystickHandler(odroidgo.BUTTON_JOY_Y, high_callback=handler.up, low_callback=handler.down)

    def poll(self):
        self.joy_x.poll()
        self.joy_y.poll()


class CrossbarPrintHandler:
    def up(self):
        print("up")

    def down(self):
        print("down")

    def right(self):
        print("right")

    def left(self):
        print("left")
