import io
import os
import sys

from odroidgo.screen import screen

TYPE_DIR = 0x4000
TYPE_FILE = 0x8000

TYPE_MAP = {TYPE_DIR: "<dir>", TYPE_FILE: "<file>"}


def dir_listing(screen, path="/"):
    screen.print("Dir listing for: %r" % path)
    try:
        for item in sorted(os.ilistdir(path)):
            item_name, item_type = item[:2]
            abs_path = "%s/%s" % (path.rstrip("/"), item_name)
            stat = os.stat(abs_path)
            human_type = TYPE_MAP.get(item_type, "<unknown>")
            screen.print("%9s %-40s %s" % (human_type, abs_path, stat))
            if item_type == TYPE_DIR:
                dir_listing(screen, path=abs_path)
    except OSError as err:
        screen.print("ERROR reading %r: %s" % (path, err))
        buffer = io.StringIO()
        sys.print_exception(err, buffer)
        content = buffer.getvalue()
        for line in content.splitlines():
            screen.print(line)


def main():
    # screen.set_font(screen.FONT_Small)
    screen.set_font(screen.FONT_DefaultSmall)
    dir_listing(screen)


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
