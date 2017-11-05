import logging

from . import api_core

logger = logging.getLogger(__name__)


async def on_server_remove(server):
    api_core.remove_server_data(server.id)
