"""
    ODROID GO Crossbar

    release value = 142

    joy-x button adc values: left 2500 - right 1200
    joy-y button adc values: up 2500 - down 1200
"""

import odroidgo


class JoystickHandler:
    def __init__(self, adc, high_callback, low_callback):
        self.adc = adc  # machine.ADC instance

        self.high_callback = high_callback
        self.low_callback = low_callback

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
        self.joy_x = JoystickHandler(odroidgo.button_joy_x_adc, high_callback=handler.left, low_callback=handler.right)
        self.joy_y = JoystickHandler(odroidgo.button_joy_y_adc, high_callback=handler.up, low_callback=handler.down)

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
