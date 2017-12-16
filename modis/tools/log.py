"""
This tool handles logging in Modis, making sure everything prints where it's
meant to go (GUI log, console, etc), and handles Unicode encoding.

Modis uses the logging package for logging. To create a new logger first import
logging, then define a logger with "logger = logging.getLogger(__name__)".
"""

import os
import time
import logging
import sys

from modis.tools import config
from modis.tools import data

logger = logging.getLogger(__name__)


class UnicodeStreamHandler(logging.StreamHandler):
    """A logging handler that supports Unicode characters."""

    def __init__(self, stream, stream_err):
        """Create a new Unicode stream handler.

        Args:
            stream: The stream to attatch the handler to.
            stream_err: The error stream to attatch the handler to.
        """

        super(UnicodeStreamHandler, self).__init__(stream)

        if not stream_err:
            stream_err = sys.stderr
        self.stream_err = stream_err

    def emit(self, record):
        """Send a formatted record into the logger output

        Args:
            record: The record to emit.
        """

        try:
            # Retrieve information from record
            msg = self.format(record)
            level = record.levelname

            # Set the stream based on the record's urgency level
            stream = self.stream
            if level in ["WARNING", "CRITICAL", "ERROR"]:
                stream = self.stream_err

            # Write to the stream
            try:
                stream.write(msg)
            except (UnicodeError, UnicodeEncodeError):
                stream.write(msg.encode("UTF-8"))

            # Exit
            stream.write(self.terminator)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def init_print(target_logger):
    """Adds a print handler to a logger.

    Args:
        target_logger (logging.logger): The logger to add the print handler to.
    """

    # Create logging directory
    if not os.path.isdir(config.LOGS_DIR):
        os.mkdir(config.LOGS_DIR)

    # Set log level
    if "log_level" not in data.cache:
        data.cache["log_level"] = "INFO"
        data.write()
    target_logger.setLevel(data.cache["log_level"])

    # Setup format
    formatter = logging.Formatter(config.LOG_FORMAT, style="{")

    # Setup handler
    handler = UnicodeStreamHandler(sys.stdout, sys.stderr)
    handler.setFormatter(formatter)

    # Add handler
    target_logger.addHandler(handler)


def init_file(target_logger):
    """Adds a file handler to a logger.

    Args:
        target_logger (logging.logger): The logger to add the file handler to.
    """

    # Create logging directory
    if not os.path.isdir(config.LOGS_DIR):
        os.mkdir(config.LOGS_DIR)

    # Set log level
    if "log_level" not in data.cache:
        data.cache["log_level"] = "INFO"
        data.write()
    target_logger.setLevel(data.cache["log_level"])

    # Setup format
    formatter = logging.Formatter(config.LOG_FORMAT, style="{")

    # Setup handlers
    handler = logging.FileHandler("{}/{}.log".format(config.LOGS_DIR, time.time()), encoding="UTF-8")
    handler.setFormatter(formatter)

    # Add handler
    target_logger.addHandler(handler)
