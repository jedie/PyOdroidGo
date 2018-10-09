# This file is executed on every boot (including wake-boot from deepsleep)

print(" *** boot.py *** ")


def print_time():
    import time

    print("time:", time.time())

    from machine import RTC

    print("RTC datetime:", RTC().now())


def led_pwm():
    import time
    import odroidgo
    from machine import Pin, PWM

    blue_led = Pin(odroidgo.LED_BLUE, Pin.OUT)
    led_pwm = PWM(blue_led, freq=1000, duty=0)

    for i in range(3, 0, -1):
        print("Boot wait %i..." % i)

        for value in range(0, 100, 10):
            led_pwm.duty(value)
            time.sleep(0.01)

        for value in range(100, 0, -10):
            led_pwm.duty(value)
            time.sleep(0.01)

    led_pwm.deinit()


def main():
    print_time()
    led_pwm()


main()
del main

import gc
gc.collect()

import micropython

# import webrepl
# webrepl.start()

# http://docs.micropython.org/en/latest/library/micropython.html#micropython.alloc_emergency_exception_buf
micropython.alloc_emergency_exception_buf(100)
