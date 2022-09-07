import logging
from pathlib import Path
from main import libs

LOG = logging.getLogger(__name__)

def test_update_file_ledger():
    """Test method."""
    search_path = Path("F:\\")

    files = libs.update_file_pointers(search_path)

    LOG.info(f"Found files: {files}")


