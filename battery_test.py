
from odroidgo.battery import OdroidGoBattery
from odroidgo.screen import screen


def main():
    battery = OdroidGoBattery()

    voltage = battery.get_voltage()
    screen.print("voltage: %sV" % voltage)

    battery.deinit()


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
