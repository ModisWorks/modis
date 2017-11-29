import logging

from . import api_core

logger = logging.getLogger(__name__)


async def on_ready():
    api_core.server_clean()
    api_core.cmd_db_update()
    logger.info("Modis for Discord is ready")
    statuslog = logging.getLogger("globalstatus")
    statuslog.info("2")
