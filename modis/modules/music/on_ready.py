from . import _musicplayer


async def on_ready():
    _musicplayer.clear_cache_root()
