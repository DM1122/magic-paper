"""Main program."""
# stdlib
from pathlib import Path

# external
import RPi.GPIO as GPIO
from inky.auto import auto
from PIL import Image

# project
from magic_paper import MagicPaper

CONFIG_PATH = Path("config.conf")


def main():
    """Main program thread."""

    # region Setup
    display = auto()
    magic_paper = MagicPaper(config_path=CONFIG_PATH, display=display)
    # endregion

    # region Update
    while True:
        if button_A:  # or timer
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
    # endregion


if __name__ == "__main__":
    main()
