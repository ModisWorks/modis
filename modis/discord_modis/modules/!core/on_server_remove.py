import logging

from .... import datatools

logger = logging.getLogger(__name__)


async def on_server_remove(server):
    logger.debug("Removing server from serverdata")
    # Remove the server from data
    data = datatools.get_data()
    if server.id in data["discord"]["servers"]:
        data["discord"]["servers"].pop(server.id)
        datatools.write_data(data)
