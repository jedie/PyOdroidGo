from odroidgo.screen import screen


def main():
    screen.print("All existing fonts:", align=screen.CENTER, color=screen.CYAN)

    fonts = screen.get_fonts()
    for font_name, font_id in fonts:
        text = "%i - %s" % (font_id, font_name)
        print(text)
        screen.set_font(font_id)
        screen.print(text, transparent=True)


if __name__ == "builtins":  # start with F5 from thonny editor ;)
    main()
