import logging

from . import api_core

logger = logging.getLogger(__name__)


async def on_ready():
    logger.info("Updating...")

    api_core.guild_clean()
    api_core.cmd_db_update()

    logger.info("Modis is ready")
    statuslog = logging.getLogger("globalstatus")
    statuslog.info("2")
