"""Magic paper class."""
# stdlib
import configparser
import logging
import os
import random
import threading
from pathlib import Path

# external
import RPi.GPIO as gpio
from PIL import Image

# project
from magic_paper import imagelib

LOG = logging.getLogger(__name__)


class MagicPaper:
    """Controller for the e-ink display."""

    def __init__(self, config_path: Path, display):
        """Initialize the controller."""
        LOG.info("Initializing controller...")

        try:
            self._load_config(config_path)
        except Exception as e:
            LOG.error(e)
            self.show_error(e)
            raise e

        self.display = display
        self.timer = None
        self.active_image = None

        # gpio pins for each button (from top to bottom)
        self.buttons = {"A": 5, "B": 6, "C": 16, "D": 24}

    def start(self):
        """Start the controller."""
        LOG.info("Starting controller...")

        self.shuffle()

    def _load_config(self, config_path: Path):
        """Load the config file."""
        if not config_path.is_file():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        if not self.config.sections():
            raise ValueError(f"Config file is empty: {config_path}")

        LOG.debug(
            f"Config file at '{config_path}' loaded with sections: {self.config.sections()}"
        )

    def _configure_gpio(self):
        """Configure the GPIO pins for buttons."""
        # Set up RPi.gpio with the "BCM" numbering scheme
        gpio.setmode(gpio.BCM)

        # Buttons connect to ground when pressed, so we should set them up
        # with a "PULL UP", which weakly pulls the input signal to 3.3V.
        for button in self.buttons.values():
            gpio.setup(button, gpio.IN, pull_up_down=gpio.PUD_UP)

        # Attach the "handle_button" function to each
        # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
        # picking a generous bouncetime to smooth out button presses.
        gpio.add_event_detect(
            self.buttons["A"],
            gpio.FALLING,
            self.shuffle,
            bouncetime=self.config["gpio"]["bouncetime"],
        )
        gpio.add_event_detect(
            self.buttons["B"],
            gpio.FALLING,
            self.rotate_image,
            bouncetime=self.config["gpio"]["bouncetime"],
        )
        gpio.add_event_detect(
            self.buttons["C"],
            gpio.FALLING,
            self.toggle_display_mode,
            bouncetime=self.config["gpio"]["bouncetime"],
        )
        gpio.add_event_detect(
            self.buttons["D"],
            gpio.FALLING,
            self.reboot,
            bouncetime=self.config["gpio"]["bouncetime"],
        )

    def shuffle(self):
        """Sample a new image from the image directory and display it."""
        LOG.info("Shuffling display image.")

        try:
            img_paths = imagelib.get_image_paths(
                search_path=Path(self.config["paths"]["images"])
            )
        except FileNotFoundError as e:
            self.show_error(e)

        if img_paths == []:
            LOG.info("No images found. Displaying default image.")
            img_path = (
                Path(self.config["paths"]["builtin_images"])
                / "missing_images.png"
            )
            img = imagelib.load_image(img_path)

            self.show(img)
            self.active_image = img_path

        else:
            img_path = random.choice(img_paths)
            img = imagelib.load_image(img_path)
            self.show(img)
            self.reset_timer()

    def reset_timer(self):
        """Reset the timer."""
        LOG.info(
            f"Setting shuffle timer for {self.config['display']['shuffle_interval']}m."
        )
        self.timer = threading.Timer(
            self.config["display"]["shuffle_interval"]*60, self.shuffle
        )
        self.timer.start()

    def rotate_active_image(self):
        """Rotate the displayed image clockwise by 90 degrees and save the
        rotation to the config."""
        angle = self.config.getint("main", "display_rotation")
        angle = (angle + 90) % 360

        self.active_image.rotate(
            angle, resample=0, expand=0, center=None, translate=None, fillcolor=None
        )

        self.config.set("main", "display_rotation", angle)

        with open("config.conf", mode="w", encoding="utf-8") as configfile:
            self.config.write(configfile)

        self.refresh_image()

    def refresh_image(self):
        """Refresh the image on the screen."""
        LOG.debug("Refreshing image.")
        self.show(self.active_image)

    def reboot(self):
        """Reboot the Pi."""
        os.system("sudo reboot")

    def toggle_display_mode(self):
        """Change the display mode between fit and fill image."""
        current_mode = self.config["display"]["mode"]

        if current_mode == "fill":
            self.config["display"]["mode"] = "fit"
        elif current_mode == "fit":
            self.config["display"]["mode"] = "fill"
        else:
            LOG.error(f"Invalid display mode: {current_mode}")
            raise ValueError(f"Invalid display mode: {current_mode}")

        with open("config.conf", mode="w", encoding="utf-8") as configfile:
            self.config.write(configfile)

        self.refresh_image()

    def show(self, img: Image, text: str = None):
        """Refresh the image on the display with the desired image.

        Creates a transparent background for the image if the image is not the right
        size.

        """
        try:
            img = self.process_image(img=img, text=text)
        except ValueError as e:
            raise ValueError(e) from e

        self.display.set_image(img)
        self.display.show()

    def process_image(self, img: Image, text: str = None):
        """Process the image."""

        if text is not None:
            img = imagelib.add_text(img=img, text=text)

        if self.config["display"]["mode"] == "fit":
            img = imagelib.fit_image(img=img, screen_size=self.display.size)

        elif self.config["display"]["mode"] == "fill":
            img = imagelib.fill_image(img=img, screen_size=self.display.size)

        else:
            raise ValueError(
                f"Invalid display mode in config: {self.config['display']['mode']}"
            )

        return img

    def show_error(self, error: Exception):
        """Display the error screen."""

        img = imagelib.load_image(
            Path(self.config["paths"]["builtin_images"]) / "error.png"
        )

        self.show(img, text=str(error))
