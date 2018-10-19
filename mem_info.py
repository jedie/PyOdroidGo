
import io
import uos
import micropython


class ScreenOut:
    def __init__(self, screen):
        self.screen = screen

    def readinto(self):
        return None
    
    def write(self, array):
        txt = bytes(array).decode("UTF-8")
        self.screen.print(txt)


def main(screen, path="/"):
    screen.print("Memory info")
    print = screen.print
    x = micropython.mem_info(False)
    print("XXX%r" % x)
    
#    screen_out = ScreenOut(screen)
#    try:
#        # https://docs.micropython.org/en/latest/library/uos.html#uos.dupterm
#        uos.dupterm(screen_out)
#        micropython.mem_info(False)
#    finally:
#        uos.dupterm(None)


print(__name__)

if __name__ == "builtins":
    from odroidgo.screen import OdroidGoDisplay

    screen = OdroidGoDisplay()
    main(screen)