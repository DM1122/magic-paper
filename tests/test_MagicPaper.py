"""Tests for MagicPaper class."""
# stdlib
import logging
import time
from ast import While
from pathlib import Path

# external
import inky.mock as inky
from PIL import Image

# project
from magic_paper import MagicPaper

LOG = logging.getLogger(__name__)

TEST_CONFIG_PATH = Path("tests/test_config.conf")


def test_init():
    """Test init."""
    display = inky.InkyMockImpression()
    paper = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)

    LOG.info(paper)
    LOG.debug(paper.config._sections)


def test_get_image_paths():
    """Test get_image_paths method."""
    display = inky.InkyMockImpression()
    paper = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)

    paths = paper._get_image_paths()

    LOG.info(paths)


def test_refresh():
    """Test refresh method."""
    display = inky.InkyMockImpression()
    paper = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)
    test_img_path = Path("tests/test_img/doggo_portrait.jpg")
    with Image.open(test_img_path) as img:
        paper.refresh(img)


def test_shuffle():
    """Test shuffle method."""
    display = inky.InkyMockImpression()
    paper = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)

    paper.shuffle()
    time.sleep(10)


def test_nonexistent_image_directory():
    """Test to make sure the missing images screen appears when image directory
    does not exist."""
    display = inky.InkyMockImpression()
    paper = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)
    paper.config["main"]["image_directory"] = "non-existent-directory/"

    paper.shuffle()


def test_empty_image_directory():
    """Test to make sure the missing images screen appears when image directory
    is empty."""
    display = inky.InkyMockImpression()
    paper = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)
    paper.config["main"]["image_directory"] = "tests/test_img/empty/"

    paper.shuffle()


def test_load_image():
    """Test load_image method."""
    display = inky.InkyMockImpression()
    paper = MagicPaper(config_path=TEST_CONFIG_PATH, display=display)
    test_img_path = Path("tests/test_img/doggo_portrait.jpg")

    img = paper._load_image(test_img_path)

    LOG.info(img)
