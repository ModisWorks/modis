import logging

from . import api_core

logger = logging.getLogger(__name__)


async def on_ready():
    api_core.check_all_servers()
    logger.info("Modis for Discord is ready")
