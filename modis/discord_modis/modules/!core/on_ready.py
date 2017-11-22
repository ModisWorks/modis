import logging

from . import api_core

logger = logging.getLogger(__name__)


async def on_ready():
    api_core.check_all_servers()
    api_core.update_cmd_db()
    logger.info("Modis for Discord is ready")
