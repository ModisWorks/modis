"""
This tool handles loggin in Modis, making sure everything prints where it's
meant to go (GUI log, console, etc), and handles Unicode encoding.

Modis uses the logging package for logging. To create a new logger first import
logging, then define a logger with "logger = logging.getLogger(__name__)".
"""


import logging


class ModisStreamHandler(logging.StreamHandler):
    """
    A handler class which allows the cursor to stay on
    one line for selected messages
    """
    def emit(self, record):
        try:
            msg = self.format(record)
            try:
                self.stream.write("{}\n".format(msg))
            except (UnicodeEncodeError, UnicodeError):
                self.stream.write("{}\n".format(msg.encode("UTF-8")))
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
    import logging
    import sys
    import time

    from modis.tools import datatools

    file_dir = os.path.dirname(os.path.realpath(__file__))

    # Create logging directory
    logs_dir = "{}/../logs/".format(file_dir)
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
    printhandler = logging.StreamHandler(sys.stdout)
    printhandler.setFormatter(formatter)
    filehandler = logging.FileHandler("{}/{}.log".format(logs_dir, time.time()))
    filehandler.setFormatter(formatter)

    logger.addHandler(printhandler)
    logger.addHandler(filehandler)

    # Initial logging messages
    logger.info("----------------NEW INSTANCE----------------")
    logger.info("Loading Modis")

    return logger
