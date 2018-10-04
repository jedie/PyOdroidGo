import time
import machine
import network

class SetupWlan:
    def __init__(self, print_func, led_pin_no=16):
        self.print_func = print_func
        self.print_func("setup WLAN...")
        self.led_pin_no = led_pin_no
        self.led_blink()

    def led_blink(self):
        import machine
        # 16 == IO16 == GPIO16 == Blue LED
        pin = machine.Pin(self.led_pin_no, machine.Pin.OUT)

        try:
            # WROOM-02
            pin.off() # turn LED on
        except AttributeError:
            # WROOM-32
            pin.value(0) # 0: turn LED on
            
        time.sleep(0.2)
        
        try:
            # WROOM-02
            pin.on() # turn LED off
        except AttributeError:
            # WROOM-32
            pin.value(1) # 0: turn LED off
        
        time.sleep(0.1)

    def connect(self):
        print("scan wlan networks...")
        self.print_func("scan WLAN...")
        wlan = network.WLAN()
        wlan.active(True)
        for info in wlan.scan():
            ssid, bssid, channel, RSSI, authmode, hidden = info
            ssid = ssid.decode("UTF-8")
            print(ssid, bssid, channel, RSSI, authmode, hidden)
            self.print_func(" * %s channel: %s hidden: %r" % (ssid, channel, hidden))

        try:
            from wlan_settings import ESSID, PASSWORD
        except ImportError as err:
            self.print_func("ERROR: %s" % err)
            self.print_func("Please create wlan_settings.py ;)")
            return
        
        if not wlan.isconnected():
            print('connecting to network...')
            self.print_func("connecting...")
            wlan.connect(ESSID, PASSWORD)
            no=0
            while not wlan.isconnected():
                no+=1
                if no>=20:
                    self.print_func("reset...")
                    time.sleep(3)
                    machine.reset()
                    
                self.led_blink()
                self.print_func("retry %i" % no)

        self.print_func("connected, IP:")
        wlan_config=wlan.ifconfig()
        print('network config:', wlan_config)
        self.print_func("%s" % wlan_config[0])

def main(lcd, print_func):
    SetupWlan(
        print_func=print_func,
        led_pin_no=2
    ).connect()
        
