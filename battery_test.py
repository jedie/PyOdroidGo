
from odroidgo.battery import OdroidGoBattery


def main(lcd, print_func):
    battery = OdroidGoBattery()

    voltage = battery.get_voltage()
    print_func("voltage: %sV" % voltage)
