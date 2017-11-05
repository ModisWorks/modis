import logging

from . import api_core

logger = logging.getLogger(__name__)


async def on_server_join(server):
    api_core.update_server_data(server.id)
