"""
    A simple battery module for Micropython, only for ODROID-GO (ESP32).

    >>> battery = OdroidGoBattery()
    >>> battery.get_voltage()
    4.868

    Created on: 2018. 7. 13 by Joshua Yang (joshua.yang@hardkernel.com)
    refactored 02.Okt.2018 by Jens Diemer
"""


from machine import ADC, Pin
from micropython import const


class Battery:
    """
    TODO: Have to calibrate the results voltage using Vref on efuse.
    But the necessary functions seem not to be implemented to MicroPython yet.

      * esp_adc_cal_characterize()
      * esp_adc_cal_raw_to_voltage()

    This module calculate current battery voltage roughly for now.
    """

    def __init__(self, battery_pin, battery_resistance_num, width, atten):
        self._adc1_pin = ADC(Pin(battery_pin))
        self._adc1_pin.width(width)
        self._adc1_pin.atten(atten)

        self._battery_resistance_num = battery_resistance_num

    def get_voltage(self, sampling_count=32, round_count=3):
        raw_value = sum([self._adc1_pin.read() for _ in range(sampling_count)]) / sampling_count
        voltage = raw_value * self._battery_resistance_num / 1000
        return round(voltage, round_count)


class OdroidGoBattery(Battery):
    def __init__(self):
        super().__init__(
            battery_pin=const(36), battery_resistance_num=const(2), width=ADC.WIDTH_12BIT, atten=ADC.ATTN_11DB
        )