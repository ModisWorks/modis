import logging

from .... import datatools

logger = logging.getLogger(__name__)


async def on_message(message):
    # Add the server to serverdata if it doesn't yet exist
    data = datatools.get_data()
    if message.server.id not in data["discord"]["servers"]:
        logger.debug("Adding new server to serverdata")
        data["discord"]["servers"][message.server.id] = {
            "prefix": "!"
        }
        datatools.write_data(data)
