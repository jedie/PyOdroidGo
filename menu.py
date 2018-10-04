import io
import os
import sys
import time

import machine
from machine import Pin
from odroidgo import buttons
from odroidgo.fonts import glcdfont, tt14, tt24, tt32
from odroidgo.lcd import get_ili9341_lcd

SKIP_NAMES = ("boot", "main", "menu")


class Starter:
    WAIT_TIME = 3
    DEFAULT_DELETE_COUNT = 3

    def __init__(self, lcd, up_pin, down_pin, run_pin, reset_pin, delete_pin):
        if lcd is not None:
            self.lcd = lcd
            self.print = lcd.print
        else:
            self.lcd = None
            self.print = print

        self.next_call = time.time() + self.WAIT_TIME
        self.pos = 0
        self.module_names = self.get_module_names()
        self.max = len(self.module_names) - 1

        self.delete_pressed = self.DEFAULT_DELETE_COUNT
        self.running = False

        min_ago = 500
        up_handler = buttons.Button(
            pin=Pin(up_pin, mode=Pin.IN, pull=Pin.PULL_UP), callback=self.up_callback, min_ago=min_ago
        )
        down_handler = buttons.Button(
            pin=Pin(down_pin, mode=Pin.IN, pull=Pin.PULL_UP), callback=self.down_callback, min_ago=min_ago
        )

        run_handler = buttons.Button(
            pin=Pin(run_pin, mode=Pin.IN, pull=Pin.PULL_UP), callback=self.run_callback, min_ago=min_ago
        )

        reset_handler = buttons.Button(
            pin=Pin(reset_pin, mode=Pin.IN, pull=Pin.PULL_UP), callback=self.reset_callback, min_ago=min_ago
        )
        delete_handler = buttons.Button(
            pin=Pin(delete_pin, mode=Pin.IN, pull=Pin.PULL_UP), callback=self.delete_callback, min_ago=min_ago
        )

        self.print_module_name()
        self.next_call = time.time() + self.WAIT_TIME

    def get_module_names(self):
        # http://docs.micropython.org/en/latest/library/uos.html#uos.ilistdir
        # collect only files, skip e.g.: directories:
        files = [item[0] for item in os.ilistdir(".") if item[1] == 0x8000]
        # print("Files: %r" % files)

        module_names = [filename.rsplit(".", 1)[0] for filename in files if not filename.startswith("_")]
        module_names = [module_name for module_name in module_names if not module_name in SKIP_NAMES]
        module_names.sort()
        for no, module_name in enumerate(module_names):
            print("%i - %r" % (no, module_name))
        return module_names

    def get_module_name(self):
        return self.module_names[self.pos]

    def print_module_name(self):
        self.print("%i - %r" % (self.pos, self.get_module_name()))

    def up_callback(self, pin):
        if self.pos <= 0:
            self.pos = self.max
        else:
            self.pos -= 1
        self.print_module_name()

    def down_callback(self, pin):
        if self.pos >= self.max:
            self.pos = 0
        else:
            self.pos += 1
        self.print_module_name()

    def run_callback(self, pin):
        if time.time() < self.next_call:
            print("Skip, next call %s" % (self.next_call - time.time()))
            return
        self.next_call = time.time() + self.WAIT_TIME

        if self.running:
            print("skip, already running")
            return
        self.running = True

        if self.lcd:
            lcd.fill(0x5500ff)

        module_name = self.get_module_name()
        self.print("import %r..." % module_name)
        module = __import__(module_name)
        self.print("Start main()...")
        try:
            module.main(self.lcd, self.print)
        except Exception as err:
            buffer = io.StringIO()
            sys.print_exception(err, buffer)
            content = buffer.getvalue()
            print(content)
            for line in content.splitlines():
                self.print(line)
        finally:
            self.print("%r done" % module_name)
            del (module)
            if lcd:
                lcd.set_font(tt24)
            self.running = False
            self.next_call = time.time() + self.WAIT_TIME

    def reset_callback(self, pin):
        if self.lcd:
            lcd.fill(0xff0000)
        self.print("Reset!")
        machine.reset()

    def delete_callback(self, pin):
        module_name = self.get_module_name()
        if self.delete_pressed >= 1:
            self.print("Delete %r ? Press again %i times." % (module_name, self.delete_pressed))
            self.delete_pressed -= 1
            return

        self.delete_pressed = self.DEFAULT_DELETE_COUNT
        self.print("delete %r" % module_name)
        try:
            os.remove("%s.py" % module_name)
        except Exception as err:
            self.print("ERROR: %s" % err)
        else:
            self.print("Deleted, ok")
            del self.module_names[self.module_names.index(module_name)]
            self.max -= 1


lcd = get_ili9341_lcd(fill=0x5500ff)
lcd.set_font(tt24)
lcd.print("start...")

starter = Starter(
    lcd=lcd,
    up_pin=buttons.BUTTON_A,
    down_pin=buttons.BUTTON_B,
    run_pin=buttons.BUTTON_START,
    reset_pin=buttons.BUTTON_MENU,
    delete_pin=buttons.BUTTON_VOLUME,
)
