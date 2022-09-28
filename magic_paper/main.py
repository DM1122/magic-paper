"""Main program."""
# stdlib
import logging
import logging.config
from pathlib import Path

# external
from inky.auto import auto

# project
from magic_paper import MagicPaper

CONFIG_PATH = Path("./magic_paper/config.conf")

# region path config
filename = Path(__file__).stem
log_path = Path(f"logs/{filename}")
# endregion

# region logging config
log_path.mkdir(parents=True, exist_ok=True)
logging.config.fileConfig(
    fname="log.conf", defaults={"path": log_path}, disable_existing_loggers=False
)
LOG = logging.getLogger(__name__)
# endregion


def main():
    """Main program thread."""

    display = auto()
    magic_paper = MagicPaper(config_path=CONFIG_PATH, display=display)

    while True:
        pass


if __name__ == "__main__":
    main()
