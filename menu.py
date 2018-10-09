import io
import os
import sys
import time

import machine
import odroidgo
from machine import Pin
from odroidgo import buttons
from odroidgo.crossbar import Crossbar
from odroidgo.screen import OdroidGoDisplay

SKIP_NAMES = ("boot", "main", "menu")


class Menu:
    WAIT_TIME = 3
    DEFAULT_DELETE_COUNT = 3

    def __init__(self, screen, reset_pin):
        if screen is not None:
            self.screen = screen
            self.print = screen.print
        else:
            self.screen = None
            self.print = print

        self.next_call = time.time() + self.WAIT_TIME
        self.pos = 0
        self.module_names = self.get_module_names()
        self.max = len(self.module_names) - 1

        self.delete_pressed = self.DEFAULT_DELETE_COUNT
        self.running = False

        reset_handler = buttons.Button(pin_no=reset_pin, callback=self.reset_callback)

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

    def up(self):
        # go one filename up
        if self.pos <= 0:
            self.pos = self.max
        else:
            self.pos -= 1
        self.print_module_name()

    def down(self):
        # go one filename down
        if self.pos >= self.max:
            self.pos = 0
        else:
            self.pos += 1
        self.print_module_name()

    def right(self):
        # start current filename
        if time.time() < self.next_call:
            print("Skip, next call %s" % (self.next_call - time.time()))
            return
        self.next_call = time.time() + self.WAIT_TIME

        if self.running:
            print("skip, already running")
            return
        self.running = True

        if self.screen:
            screen.reset()

        module_name = self.get_module_name()
        self.print("import %r..." % module_name)
        module = __import__(module_name)
        self.print("Start main()...")
        try:
            module.main(self.screen, self.print)
        except Exception as err:
            buffer = io.StringIO()
            sys.print_exception(err, buffer)
            content = buffer.getvalue()
            print(content)
            if screen:
                screen.set_default_font()
            for line in content.splitlines():
                self.print(line)
        finally:
            # try to 'reset' everything
            self.print("%r done" % module_name)
            del (module)
            del (sys.modules[module_name])

        if screen:
            screen.set_default_font()
        self.running = False
        self.next_call = time.time() + self.WAIT_TIME
        self.print_module_name()

    def reset_callback(self, pin):
        if self.screen:
            screen.fill(0xff0000)
            screen.reset_scroll()
            screen.set_pos(0, 0)
        self.print("Reset!")
        machine.reset()

    def left(self):
        # delete current file
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
            self.print_module_name()


screen = OdroidGoDisplay()
screen.print("PyOdroidGo by Jens Diemer (GPLv3)")
screen.print(
    "%s %s on %s (Python v%s)"
    % (sys.implementation.name, ".".join([str(i) for i in sys.implementation.version]), sys.platform, sys.version)
)

try:
    menu = Menu(screen=screen, reset_pin=odroidgo.BUTTON_MENU)
    crossbar = Crossbar(handler=menu)
    while True:
        crossbar.poll()
        time.sleep(0.1)
finally:
    screen.deinit()
    print("--END--")
