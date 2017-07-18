import logging

import datetime
import sys
import traceback

logger = logging.getLogger(__name__)


async def on_error(event_method, *args, **kwargs):
    # Print error prettily
    print("\n"
          + "################################\n"
          + "ERROR\n"
          + str(datetime.datetime.now()).split('.')[0] + "\n"
          + ''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
          + "################################\n\n")
