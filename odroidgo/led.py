"""
    ODROID GO LEDs
"""

import odroidgo
from machine import Pin

blue_led = Pin(odroidgo.LED_BLUE, Pin.OUT)
