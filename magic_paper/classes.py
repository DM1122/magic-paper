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

LOG = logging.getLogger(__name__)


class MagicPaper:
    """Controller for the e-ink display."""

    def __init__(self, config_path: Path, display):
        """Initialize the controller."""
        LOG.info("Initializing controller...")
        self.display = display
        self.active_image = None

        # region load config
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        assert (
            self.config.sections() != []
        ), f"Config file at '{config_path}' could not be loaded correctly."
        LOG.debug(f"Config file at '{config_path}' loaded: {self.config.sections()}")
        # endregion

        # region config io
        # gpio pins for each button (from top to bottom)
        self.buttons = {"A": 5, "B": 6, "C": 16, "D": 24}
        self.button_bouncetime = 250  # ms

        # Set up RPi.gpio with the "BCM" numbering scheme
        gpio.setmode(gpio.BCM)

        # Buttons connect to ground when pressed, so we should set them up
        # with a "PULL UP", which weakly pulls the input signal to 3.3V.
        for button in self.buttons.values():
            gpio.setup(button, gpio.IN, pull_up_down=gpio.PUD_UP)

        # Attach the "handle_button" function to each
        # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
        # picking a generous bouncetime to smooth out button presses.
        # gpio.add_event_detect(
        #     self.buttons["A"],
        #     gpio.FALLING,
        #     self.shuffle,
        #     bouncetime=self.button_bouncetime,
        # )
        # gpio.add_event_detect(
        #     self.buttons["B"],
        #     gpio.FALLING,
        #     self.rotate_image,
        #     bouncetime=self.button_bouncetime,
        # )
        # gpio.add_event_detect(
        #     self.buttons["C"],
        #     gpio.FALLING,
        #     self.toggle_display_mode,
        #     bouncetime=self.button_bouncetime,
        # )
        # gpio.add_event_detect(
        #     self.buttons["D"],
        #     gpio.FALLING,
        #     self.reboot,
        #     bouncetime=self.button_bouncetime,
        # )
        # endregion

        self.shuffle()

    def shuffle(self):
        """Sample a new image from the image directory and display it."""
        LOG.info("Shuffling display image.")
        img_paths = self._get_image_paths()
        if img_paths == []:  # display the missing images screen
            LOG.info("No images found. Displaying default image.")
            img = self._load_image(
                Path(self.config["main"]["builtin_image_directory"])
                / "missing-images.png"
            )
            self.show(img)
        else:
            img_path = random.choice(img_paths)
            img = self._load_image(img_path)
            self.show(img)
            self.reset_timer()

    def reset_timer(self):
        """Reset the timer."""
        LOG.info(
            f"Setting shuffle timer for {self.config['main']['shuffle_image_interval']}s."
        )
        self.timer = threading.Timer(
            self.config["main"]["shuffle_image_interval"], self.shuffle
        )
        self.timer.start()

    def rotate_image(self):
        """Rotate the displayed image clockwise by 90 degrees and save the
        rotation to the config."""
        LOG.info("Rotating image.")
        angle = self.config.getint("main", "display_rotation")
        angle = (angle + 90) % 360

        self.active_image.rotate(
            angle, resample=0, expand=0, center=None, translate=None, fillcolor=None
        )

        self.config.set("main", "display_rotation", angle)

        with open("config.conf", "w") as configfile:
            self.config.write(configfile)

        self.refresh_image()

    def reboot(self):
        """Reboot the Pi."""
        os.system("sudo reboot")

    def update_config(self):
        pass

    def toggle_display_mode(self):
        """Change the display mode between fit and no fit image."""
        fit_image = config.getboolean("main", "fit_image")
        fit_image = not fit_image

        config.set("main", "fit_image", fit_image)

        with open("config.conf", "w") as configfile:
            config.write(configfile)

        self.show()

    def show(self, img: Image):
        """Refresh the image on the display with the desired image.

        Creates a transparent background for the image if the image is not the right
        size.

        """
        try:
            img = self._process_image(img)
        except ValueError as e:
            raise ValueError(e) from e

        self.display.set_image(img)
        self.display.show()
        self.active_image = img

    def _process_image(self, img: Image):
        """Process the image to fit the display."""
        if self.config["main"]["display_mode"] == "fit":
            img.thumbnail(self.display.resolution)
            bg = Image.new("RGBA", self.display.resolution, (0, 0, 0, 0))
            bg.paste(img, (0, 0))
            img = bg

        elif self.config["main"]["display_mode"] == "fill":
            img = img.resize(self.display.resolution)
            img = img.crop((0, 0, *self.display.resolution))  # TODO: center crop

        else:
            LOG.error(
                f"Invalid display mode in config: {self.config['main']['display_mode']}"
            )
            raise ValueError(
                f"Invalid display mode in config: {self.config['main']['display_mode']}"
            )

        return img

    def _load_image(self, path: Path):
        """Load an image from a path."""
        img = Image.open(path).convert(
            "RGBA"
        )  # convert to RGBA to support transparency for fit image mode
        LOG.debug(f"Loaded image from {path}: {img}")

        return img

    def _get_image_paths(self):
        """Get the paths to all images in the image directory."""
        search_dir = Path(self.config["main"]["image_directory"])

        if search_dir.is_dir():
            paths = sorted(search_dir.rglob("*"))
            img_paths = [path for path in paths if path.is_file()]
            if img_paths == []:
                LOG.warning("No images found in directory.")
        else:
            LOG.error("Image directory not found.")
            img_paths = []

        return img_paths
