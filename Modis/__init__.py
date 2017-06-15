def run(apikeys, client_id="", game="", prefix="!"):
    """Runs Modis

    Args:
        apikeys (dict): The API keys required to run Modis and its modules
        client_id (str): The client id of the bot Modis will run on; used to make the invite link
        game (str): The game Modis will be playing; defaults to ""
        prefix (str): The prefix to use for Modis commands; defaults to '!'
    """

    # Import global variable bank
    import share

    # Register variables globally
    share.apikeys = apikeys
    share.client_id = client_id
    share.game = game
    share.prefix = prefix

    # Start console
    import console
    console.init()
