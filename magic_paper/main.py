"""Main program."""
# stdlib
import random
from pathlib import Path

# external
from inky.auto import auto
from PIL import Image

# project
from magic_paper import MagicPaper

CONFIG_PATH = Path("config.conf")


def main():
    """Main program thread."""
    magic_paper = MagicPaper(config_path=CONFIG_PATH)

    while True:

        if timer or button_A:
            img = libs.shuffle_image()
            display.set_image(img)
            timer.restart()
            inky_display.show()

        if button_B:
            libs.rotate_image()

        if button_C:
            libs.toggle_display_mode()

        if button_D:
            libs.reboot()


if __name__ == "__main__":
    main()
