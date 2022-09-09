"""Magic paper class."""
# stdlib
import configparser
import logging
import random
from pathlib import Path

# external
from PIL import Image

LOG = logging.getLogger(__name__)


class MagicPaper:
    """Controller for the e-ink display."""

    def __init__(self, config_path: Path, display):
        """Initialize the controller."""
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.display = display
        self.active_image = None

    def shuffle(self):
        """Sample a new image from the image directory and display it."""
        img_paths = self._get_image_paths()
        if img_paths == []:  # display the missing images screen
            img = self._load_image(
                Path(self.config["main"]["builtin_image_directory"])
                / "missing_images.png"
            )
            self.show(img)
        else:
            img_path = random.choice(img_paths)
            img = self._load_image(img_path)
            self.show(img)

    def rotate_image(self):
        """Rotate the displayed image clockwise by 90 degrees and save the
        rotation to the config."""
        angle = self.config.getint("main", "display_rotation")
        angle = (angle + 90) % 360

        self.active_image.rotate(
            angle, resample=0, expand=0, center=None, translate=None, fillcolor=None
        )

        self.config.set("main", "display_rotation", angle)

        with open("config.conf", "w") as configfile:
            config.write(configfile)

        self.refresh_image()

    def reboot(self):
        """Reboot the Pi."""
        pass

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
