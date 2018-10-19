# This file is executed on every boot (including wake-boot from deepsleep)

print(" *** boot.py *** ")

def main():
    import time
    print("time:", time.time())

    from machine import RTC
    print("RTC datetime:", RTC().now())


main()
del main

import gc
gc.collect()

import micropython

# import webrepl
# webrepl.start()

# http://docs.micropython.org/en/latest/library/micropython.html#micropython.alloc_emergency_exception_buf
micropython.alloc_emergency_exception_buf(100)
