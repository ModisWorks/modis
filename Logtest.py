import logging
import sys

logstdout = logging.StreamHandler(sys.stdout)

# logging.Logger("modis")
logging.getLogger("modis").setLevel("DEBUG")
# logging.Logger("modis.bar")
logging.getLogger("modis.bar").setLevel("DEBUG")

logging.getLogger("modis").addHandler(logstdout)

logging.getLogger("modis").debug("Testing")
logging.getLogger("modis.bar").error("Test2")
