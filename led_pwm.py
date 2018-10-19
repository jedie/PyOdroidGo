import time

from machine import PWM, Pin
from odroidgo.led import blue_led
from odroidgo.screen import screen


def main():
    led_pwm = PWM(blue_led, freq=1000, duty=0)

    for i in range(3, 0, -1):
        screen.print("%i" % i)

        for value in range(0, 100, 10):
            led_pwm.duty(value)
            time.sleep(0.01)

        for value in range(100, 0, -10):
            led_pwm.duty(value)
            time.sleep(0.01)

    led_pwm.deinit()


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
