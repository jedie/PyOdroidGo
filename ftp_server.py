import time

import machine
import network
from odroidgo.screen import screen


def main():
    try:
        from wlan_settings import SSID, PASSWORD
    except ImportError as err:
        screen.print("ERROR: %s" % err)
        screen.print("Please create wlan_settings.py with SSID, PASSWORD ;)")
        raise RuntimeError

    # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/network

    screen.print("Activate WLAN")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    screen.print("scan...")
    for info in wlan.scan(True):
        ssid, bssid, primary_chan, rssi, auth_mode, auth_mode_string, hidden = info
        ssid = ssid.decode("UTF-8")
        if hidden:
            hidden = "hidden!"
        else:
            hidden = ""
        screen.print(" * %-20s channel %02i %s%s" % (ssid, primary_chan, auth_mode_string, hidden))

    if not wlan.isconnected():
        screen.print("connecting to network...")
        wlan.connect(SSID, PASSWORD)
        no = 0
        while not wlan.isconnected():
            no += 1
            if no >= 20:
                screen.print("reset...")
                time.sleep(3)
                machine.reset()
            time.sleep(1)

    screen.print("connected, IP:")
    wlan_config = wlan.ifconfig()
    screen.print("network config: %s" % repr(wlan_config))

    # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/rtc
    screen.print("NTP time...")
    rtc = machine.RTC()
    rtc.init((2018, 1, 1, 12, 12, 12))

    # found in second field, text before the coma, in
    # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/blob/master/MicroPython_BUILD/components/micropython/docs/zones.csv
    my_timezone = "CET-1CEST,M3.5.0,M10.5.0/3"  # Europe/Berlin

    rtc.ntp_sync(server="pool.ntp.org", tz=my_timezone, update_period=3600)

    screen.print("time: %s" % repr(rtc.now()))

    # https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/ftpserver

    screen.print("Start FTP Server...")
    network.ftp.start(user="micro", password="python", buffsize=1024, timeout=300)
    # network.telnet.start(user="micro", password="python", timeout=300)

    screen.print("done.")


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
