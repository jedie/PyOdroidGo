import os

TYPE_DIR = 0x4000
TYPE_FILE = 0x8000

TYPE_MAP = {TYPE_DIR: "<dir>", TYPE_FILE: "<file>"}


def dir_listing(path="/"):
    try:
        for item in sorted(os.ilistdir(path)):
            item_name, item_type = item[:2]
            abs_path = "%s/%s" % (path.rstrip("/"), item_name)
            stat = os.stat(abs_path)
            human_type = TYPE_MAP.get(item_type, "<unknown>")
            print("%9s %-40s %s" % (human_type, abs_path, stat))
            if item_type == TYPE_DIR:
                dir_listing(path=abs_path)
    except OSError as err:
        print("ERROR reading %r: %s" % (path, err))


dir_listing(path="/")
