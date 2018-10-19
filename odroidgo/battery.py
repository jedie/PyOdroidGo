"""
    ODROID-GO battery

    >>> battery = OdroidGoBattery()
    >>> battery.get_voltage()
    4.868

    Created on: 2018. 7. 13 by Joshua Yang (joshua.yang@hardkernel.com)
    refactored Okt.2018 by Jens Diemer
"""


import odroidgo
from machine import ADC, Pin


class Battery:
    """
    TODO: Have to calibrate the results voltage using Vref on efuse.
    But the necessary functions seem not to be implemented to MicroPython yet.

      * esp_adc_cal_characterize()
      * esp_adc_cal_raw_to_voltage()

    This module calculate current battery voltage roughly for now.
    """

    def __init__(self, battery_pin, battery_resistance_num, width, atten):
        self._battery_adc = ADC(Pin(battery_pin))
        self._battery_adc.width(width)
        self._battery_adc.atten(atten)

        self._battery_resistance_num = battery_resistance_num

    def get_voltage(self, sampling_count=32, round_count=3):
        raw_value = sum([self._battery_adc.read() for _ in range(sampling_count)]) / sampling_count
        voltage = raw_value * self._battery_resistance_num / 1000
        return round(voltage, round_count)

    def deinit(self):
        """ Deinitialize the battery pin ADC """
        self._battery_adc.deinit()


class OdroidGoBattery(Battery):
    def __init__(self):
        super().__init__(
            battery_pin=odroidgo.BATTERY_PIN,
            battery_resistance_num=odroidgo.BATTERY_RESISTANCE_NUM,
            width=ADC.WIDTH_12BIT,
            atten=ADC.ATTN_11DB,
        )
