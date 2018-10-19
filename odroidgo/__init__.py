"""
    ODROID GO constants
"""

from machine import ADC, Pin
from micropython import const

TFT_MISO_PIN = const(19)
TFT_MOSI_PIN = const(23)
TFT_SCLK_PIN = const(18)

TFT_CS_PIN = const(5)
TFT_DC_PIN = const(21)

TFT_WIDTH = const(320)
TFT_HEIGHT = const(240)
TFT_SPEED = const(40000000)

BUTTON_MENU = const(13)
BUTTON_VOLUME = const(0)
BUTTON_SELECT = const(27)
BUTTON_START = const(39)

BUTTON_A = const(32)
BUTTON_B = const(33)

BUTTON_JOY_X = const(34)
BUTTON_JOY_Y = const(35)

BUTTON_JOY_MIN_ADC = const(200)
BUTTON_JOY_MIN_ADC_HIGH = const(2500)
BUTTON_JOY_MIN_ADC_LOW = const(1200)

LED_BLUE = const(2)

BATTERY_PIN=const(36)
BATTERY_RESISTANCE_NUM=const(2)


#_____________________________________________________________________________
# ODROID GO object instances


# set PULL_UP will raise into:
# ValueError: pins 34~39 do not have pull-up or pull-down circuitry
button_joy_x_pin = Pin(BUTTON_JOY_X, mode=Pin.IN)  # , pull=Pin.PULL_UP)
button_joy_x_adc = ADC(button_joy_x_pin)
button_joy_x_adc.width(ADC.WIDTH_9BIT)
button_joy_x_adc.atten(ADC.ATTN_11DB)

button_joy_y_pin = Pin(BUTTON_JOY_Y, mode=Pin.IN)  # , pull=Pin.PULL_UP)
button_joy_y_adc = ADC(button_joy_y_pin)
button_joy_y_adc.width(ADC.WIDTH_9BIT)
button_joy_y_adc.atten(ADC.ATTN_11DB)