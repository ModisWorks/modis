"""
This tool handles logging in Modis, making sure everything prints where it's
meant to go (GUI log, console, etc), and handles Unicode encoding.

Modis uses the logging package for logging. To create a new logger first import
logging, then define a logger with "logger = logging.getLogger(__name__)".
"""

import logging
import sys


class UnicodeStreamHandler(logging.StreamHandler):
    """A handler for Modis' logging and Unicode characters"""

    def __init__(self, stream, stream_err):
        super(UnicodeStreamHandler, self).__init__(stream)

        if not stream_err:
            stream_err = sys.stderr
        self.stream_err = stream_err

    def emit(self, record):
        try:
            msg = self.format(record)
            level = getattr(record, "levelname")

            stream = self.stream
            if level in ["WARNING", "CRITICAL", "ERROR"]:
                stream = self.stream_err

            try:
                stream.write(msg)
            except (UnicodeError, UnicodeEncodeError):
                stream.write(msg.encode("UTF-8"))

            stream.write(self.terminator)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def init_print(logger):
    """Adds a print handler to a logger

    Args:
        logger (logging.logger): The logger to add the print handler to.
    """

    import os

    from modis.tools import config
    from modis.tools import data

    # Create logging directory
    if not os.path.isdir(config.LOGS_DIR):
        os.mkdir(config.LOGS_DIR)

    # Set log level
    if "log_level" not in data.cache:
        data.cache["log_level"] = "INFO"
        data.write()
    logger.setLevel(data.cache["log_level"])

    # Setup format
    formatter = logging.Formatter(config.LOG_FORMAT, style="{")

    # Setup handler
    handler = UnicodeStreamHandler(sys.stdout, sys.stderr)
    handler.setFormatter(formatter)

    # Add handler
    logger.addHandler(handler)


def init_file(logger):
    """Adds a file handler to a logger

    Args:
        logger (logging.logger): The logger to add the file handler to.
    """

    import os
    import time

    from modis.tools import config
    from modis.tools import data

    # Create logging directory
    if not os.path.isdir(config.LOGS_DIR):
        os.mkdir(config.LOGS_DIR)

    # Set log level
    if "log_level" not in data.cache:
        data.cache["log_level"] = "INFO"
        data.write()
    logger.setLevel(data.cache["log_level"])

    # Setup format
    formatter = logging.Formatter(config.LOG_FORMAT, style="{")

    # Setup handlers
    handler = logging.FileHandler("{}/{}.log".format(config.LOGS_DIR, time.time()), encoding="UTF-8")
    handler.setFormatter(formatter)

    # Add handler
    logger.addHandler(handler)
