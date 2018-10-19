import time

from machine import PWM, Pin
from odroidgo.led import blue_led


def main(screen):
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


if __name__ == "builtins":
    from odroidgo.screen import OdroidGoDisplay

    screen = OdroidGoDisplay()
    main(screen)
    screen.deinit()
    del screen
    print("---END---")
