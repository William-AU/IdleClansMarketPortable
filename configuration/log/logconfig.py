import platform
import logging

logger = logging.getLogger(__name__)
from backend.storage.storage_path_utils import get_or_create_log_path

"""Assumed to be raspberry pi setup"""


def _setup_logging_linux():
    log_path = get_or_create_log_path()
    logging.basicConfig(filename=get_or_create_log_path() + "IdleClansMarket.log", level=logging.INFO)
    logger.info("Logging set up for raspberry pie")


"""Assumed to be debugging setup"""


def _setup_logging_windows():
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Logging set up for debugging")


def setup_logging():
    system = platform.system()
    if system == "Windows":
        _setup_logging_windows()
    else:
        _setup_logging_linux()
