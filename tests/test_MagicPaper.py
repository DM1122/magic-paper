"""Tests for MagicPaper class."""
# stdlib
import logging
import time
from pathlib import Path

# external
import inky.mock as inky
import pytest
from PIL import Image

# project
from magic_paper import MagicPaper

LOG = logging.getLogger(__name__)

TEST_CONFIG_PATH = Path("tests/test_config.conf")


def test_init():
    """Test init."""
    display = inky.InkyMockImpression()
    controller = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)

    LOG.info(controller)
    LOG.debug(controller.config._sections)


def test_show():
    """Test show method."""
    display = inky.InkyMockImpression()
    controller = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)
    test_img_path = Path("tests/test_img/doggo_portrait.jpg")
    img = Image.open(test_img_path)
    controller.show(img)


def test_shuffle():
    """Test shuffle method."""
    display = inky.InkyMockImpression()
    controller = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)

    controller.shuffle()


@pytest.mark.parametrize(
    "mode, exception", [("fill", None), ("fit", None), ("fake", ValueError)]
)
def test_process_image_fit(mode, exception):
    """Test process_image method with fit mode."""
    display = inky.InkyMockImpression()
    controller = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)
    test_img_path = Path("tests/test_img/doggo_portrait.jpg")

    img = controller.load_image(test_img_path)
    controller.config["main"]["display_mode"] = mode

    if exception is None:
        img = controller.process_image(img)
    else:
        with pytest.raises(exception):
            img = controller.process_image(img)

    LOG.info(img)


def test_load_image():
    """Test load_image method."""
    display = inky.InkyMockImpression()
    controller = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)
    test_img_path = Path("tests/test_img/doggo_portrait.jpg")

    img = controller.load_image(test_img_path)

    LOG.info(img)


def test_get_image_paths():
    """Test get_image_paths method."""
    display = inky.InkyMockImpression()
    controller = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)

    paths = controller.get_image_paths()

    LOG.info(paths)
