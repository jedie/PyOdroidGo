import time

import machine
from odroidgo.screen import screen


def main():
    for i in range(5, 0, -1):
        screen.echo("Hard reset in %i Sek!" % i)
        time.sleep(1)

    screen.echo("reset...")
    machine.reset()


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
