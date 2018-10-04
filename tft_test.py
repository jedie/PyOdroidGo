import time

from odroidgo.fonts import glcdfont, tt14, tt24, tt32
from odroidgo.lcd import get_ili9341_lcd

FONTS = (glcdfont, tt14, tt24, tt32)

def main(lcd, print_func):
    if lcd is None:
        lcd = get_ili9341_lcd(fill=0x5500ff)
        lcd.print("Hello World!")
        
    for font in FONTS:
        lcd.set_font(font)
        lcd.print("%s %s" % (font.__name__, time.time()))
