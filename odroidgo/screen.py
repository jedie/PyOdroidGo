"""
    ODROID GO display

    https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/display
"""

import sys
import time

import display
import machine
import odroidgo
from machine import SPI, Pin
from micropython import const


class Display(display.TFT):
    """
    Expand loboris TFT class
    """

    def __init__(self, **init_kwargs):
        super().__init__()

        try:
            self.init(**init_kwargs)
        except OSError as err:
            # e.g.: Error initializing display
            sys.print_exception(err)
            for i in range(3, 0, -1):
                print("Hard reset in %i Sek!" % i)
                time.sleep(1)
            machine.reset()

        self.width, self.height = self.screensize()
        self.reset()

    def reset(self):
        self.resetwin()  # Reset active display window to full screen size
        self.clear(self.BLACK)
        self.set_default_font()
        self.text(0, 0, "", self.BLACK)
        self.text_next_y=0

    def set_default_font(self):
        self.set_font(self.FONT_Default)

    def get_fonts(self):
        fonts = [(attr_name, getattr(self, attr_name)) for attr_name in dir(self) if attr_name.startswith("FONT_")]
        fonts.sort(key=lambda i: i[1])
        return tuple(fonts)

    def set_font(self, font_id, rotate=0):
        self.font(font_id, rotate=rotate)
        self.font_width, self.font_height = self.fontSize()

    def print(self, text, align=0, color=None, transparent=False):
        if color is None:
            color = self.WHITE

        if self.text_next_y >= self.height:
            self.text_next_y = 0
            
        self.text(align, self.text_next_y, text, color, transparent=transparent)
        self.text_next_y = self.text_y() + self.font_height


class OdroidGoDisplay(Display):
    """
    ODROID GO TFT

    usage e.g.:

        screen = OdroidGoDisplay()
        screen.print("All existing fonts:", align=screen.CENTER, color=screen.CYAN)

        fonts = screen.get_fonts()
        for font_name, font_id in fonts:
            text = "%i - %s" % (font_id, font_name)
            print(text)
            screen.set_font(font_id)
            screen.print(text, transparent=True)

        screen.deinit()
    """

    def __init__(self):
        super().__init__(
            type=self.ILI9341,
            width=odroidgo.TFT_WIDTH,
            height=odroidgo.TFT_HEIGHT,
            speed=odroidgo.TFT_SPEED,
            miso=odroidgo.TFT_MISO_PIN,
            mosi=odroidgo.TFT_MOSI_PIN,
            clk=odroidgo.TFT_SCLK_PIN,
            cs=odroidgo.TFT_CS_PIN,
            spihost=SPI.VSPI,
            dc=odroidgo.TFT_DC_PIN,
            bgr=True,
            rot=self.LANDSCAPE_FLIP,
        )
