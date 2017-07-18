import logging

from .... import datatools

logger = logging.getLogger(__name__)


async def on_server_join(server):
    # Add the server to serverdata if it doesn't yet exist
    data = datatools.get_data()
    if server.id not in data["servers"]:
        logger.debug("Adding new server to serverdata")
        data["servers"][server.id] = {
            "prefix": "!"
        }
        datatools.write_data(data)
