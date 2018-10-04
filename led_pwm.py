from machine import Pin, PWM
from micropython import const

import time

def main(lcd, print_func):
    BLUE_LED = const(2)
    blue_led = Pin(BLUE_LED, Pin.OUT)
    led_pwm = PWM(blue_led, freq=1000, duty=0)

    for i in range(3, 0, -1):
        print_func("%i" % i)

        for value in range(0, 1023, 100):
            led_pwm.duty(value)
            time.sleep(0.05)

        for value in range(1023, 0, -100):
            led_pwm.duty(value)
            time.sleep(0.05)

    led_pwm.deinit()

