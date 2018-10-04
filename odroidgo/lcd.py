import time

import machine
from machine import SPI, Pin
from micropython import const

from .fonts import glcdfont, tt14, tt24, tt32
from .ili934x import ILI9341


def get_ili9341_lcd(fill=0x5500ff):
    TFT_MISO_PIN = const(19)
    TFT_MOSI_PIN = const(23)
    TFT_SCLK_PIN = const(18)

    TFT_CS_PIN = const(5)
    TFT_DC_PIN = const(21)

    try:
        print("make SPI instance")
        spi = SPI(2)  # will raise in SPI device already in use
        print("deinit")
        spi.deinit()
        print("init")
        spi.init(
            baudrate=40000000,
            miso=Pin(TFT_MISO_PIN, Pin.IN),
            mosi=Pin(TFT_MOSI_PIN, Pin.OUT),
            sck=Pin(TFT_SCLK_PIN, Pin.OUT),
        )
    except OSError as err:
        # e.g.: SPI device already in use
        print("ERROR: %s" % err)
        for i in range(3, 0, -1):
            print("Hard reset in %i Sek!" % i)
            time.sleep(1)
        machine.reset()
    else:
        lcd = ILI9341(spi, cs=Pin(TFT_CS_PIN, Pin.OUT), dc=Pin(TFT_DC_PIN, Pin.OUT), font=glcdfont)
        lcd.fill(fill)
        return lcd
