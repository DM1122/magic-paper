"""Magic paper class."""
# stdlib
import logging
from pathlib import Path

# external
from PIL import Image

LOG = logging.getLogger(__name__)


def load_image(path: Path):
    """Load an image from a path."""
    img = Image.open(path).convert(
        "RGBA"
    )  # convert to RGBA to support transparency for fit image mode
    LOG.debug(f"Loaded image from {path}: {img}")

    return img


def rotate_image(img: Image, angle: int):
    """Rotate image."""

    angle = angle % 360

    img.rotate(angle, resample=0, expand=0, center=None, translate=None, fillcolor=None)
    return img


def fit_image(img: Image, screen_size: tuple):
    """Fit image to screen size."""

    img.thumbnail(screen_size)

    bg = Image.new("RGBA", screen_size, (255, 255, 255, 255))
    bg.paste(img, (bg.size[0] / 2 - img.size[0], bg.size[1] / 2 - img.size[1]))

    img = bg

    return img


def fill_image(img: Image, screen_size: tuple):
    """Fill screen with image."""
    img = img.resize(screen_size)
    img = img.crop((0, 0, *screen_size))  # TODO: center crop

    return img


def get_image_paths(search_path: Path):
    """Get the paths to all images in the image directory."""

    if search_path.is_dir():
        paths = sorted(search_path.rglob("*"))
        img_paths = [path for path in paths if path.is_file()]

        if img_paths == []:
            LOG.warning("No images found in directory.")
    else:
        LOG.error("Image directory not found.")
        raise FileNotFoundError(f"Image directory not found: {search_path}")

    return img_paths


def add_text(img: Image, text: str):
    """Add text to image."""
    img.text((28, 36), text, fill=(0, 0, 0))

    return img
