"""Magic paper class."""
# stdlib
import logging
from pathlib import Path

# external
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

LOG = logging.getLogger(__name__)


def load_image(path: Path):
    """Load an image from a path."""
    img = Image.open(path).convert(
        "RGBA"
    )  # convert to RGBA to support transparency for fit image mode
    img = ImageOps.exif_transpose(image=img)
    LOG.debug(f"Loaded image from {path}: {img}")

    return img


def rotate_image(img: Image, angle: int):
    """Rotate image."""
    LOG.debug("Rotating image")
    img = img.rotate(angle, expand=True, fillcolor=(0, 0, 0, 255))
    return img


def fit_image(img: Image, screen_size: tuple[int, int]):
    """Fit image to screen size."""

    img.thumbnail(screen_size)

    bg = Image.new(mode="RGBA", size=screen_size, color=(255, 255, 255, 255))
    bg.paste(
        im=img,
        box=(bg.size[0] // 2 - img.size[0] // 2, bg.size[1] // 2 - img.size[1] // 2),
    )

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
