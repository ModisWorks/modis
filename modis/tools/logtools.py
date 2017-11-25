"""
This tool handles loggin in Modis, making sure everything prints where it's
meant to go (GUI log, console, etc), and handles Unicode encoding.

Modis uses the logging package for logging. To create a new logger first import
logging, then define a logger with "logger = logging.getLogger(__name__)".
"""

import logging
import sys


class ModisStreamHandler(logging.StreamHandler):
    """
    A handler for Modis' logging and Unicode characters
    """

    def __init__(self, stream, stream_err):
        super(ModisStreamHandler, self).__init__(stream)
        if stream_err is None:
            stream_err = sys.stderr
        self.stream_err = stream_err

    def emit(self, record):
        try:
            msg = self.format(record)
            level = getattr(record, "levelname")

            stream = self.stream
            if level in ["CRITICAL", "ERROR"]:
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


def log_init():
    """Initialises the root logger.

    Returns:
        logger (logging.logger): The root logger.
    """

    import os
    import time

    from modis.tools import datatools

    working_dir = os.path.realpath(os.getcwd())

    # Create logging directory
    logs_dir = "{}/logs/".format(working_dir)
    if not os.path.isdir(logs_dir):
        os.mkdir(logs_dir)

    # Create logger
    logger = logging.getLogger(__name__)

    # Set log level
    data = datatools.get()
    if "log_level" in data:
        logger.setLevel(data["log_level"])
    else:
        data["log_level"] = "INFO"
        datatools.write(data)
        logger.setLevel("INFO")

    # Setup logging format
    formatter = logging.Formatter("{asctime} {levelname:8} {name} - {message}",
                                  style="{")

    # Setup logging handlers
    printhandler = ModisStreamHandler(sys.stdout, sys.stderr)
    printhandler.setFormatter(formatter)
    filehandler = logging.FileHandler("{}/{}.log".format(logs_dir, time.time()),
                                      encoding="UTF-8")
    filehandler.setFormatter(formatter)

    logger.propagate = False
    logger.addHandler(printhandler)
    logger.addHandler(filehandler)

    # Initial logging messages
    logger.info("----------------NEW INSTANCE----------------")
    logger.info("Loading Modis")

    return logger
