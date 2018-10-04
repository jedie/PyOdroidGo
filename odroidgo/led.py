from machine import Pin
from micropython import const

BLUE_LED = const(2)
blue_led = Pin(BLUE_LED, Pin.OUT)