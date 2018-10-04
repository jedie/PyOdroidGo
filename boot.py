# This file is executed on every boot (including wake-boot from deepsleep)

print("boot.py")

import time
print("time:", time.time())

from machine import Pin
from micropython import const

from machine import RTC
print("RTC datetime:", RTC().datetime())


def led_pwm():
    BLUE_LED = const(2)
    blue_led = Pin(BLUE_LED, Pin.OUT)
    
    from machine import PWM
    led_pwm = PWM(blue_led, freq=1000, duty=0)

    for i in range(3, 0, -1):
        print("Boot wait %i..." % i)

        for value in range(0, 1023, 100):
            led_pwm.duty(value)
            time.sleep(0.01)

        for value in range(1023, 0, -100):
            led_pwm.duty(value)
            time.sleep(0.01)

    led_pwm.deinit()

led_pwm()


import gc
#import webrepl
#webrepl.start()
gc.collect()