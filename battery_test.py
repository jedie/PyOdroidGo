
from odroidgo.battery import OdroidGoBattery


def main(screen):
    battery = OdroidGoBattery()

    voltage = battery.get_voltage()
    screen.print("voltage: %sV" % voltage)

    battery.deinit()
