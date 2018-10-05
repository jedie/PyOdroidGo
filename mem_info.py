
import io
import os
from odroidgo import fonts
import micropython


class LcdOut(io.IOBase):
    def __init__(self, lcd):
        self.lcd = lcd

    def readinto(self):
        return None
    
    def write(self, array):
        txt = bytes(array).decode("UTF-8")
        self.lcd.write(txt)


def main(lcd, print_func):   
    lcd_out = LcdOut(lcd)
    lcd.set_font(fonts.glcdfont)
    try:
        # https://docs.micropython.org/en/latest/library/uos.html#uos.dupterm
        os.dupterm(lcd_out)
        micropython.mem_info(False)
    finally:
        os.dupterm(None)
