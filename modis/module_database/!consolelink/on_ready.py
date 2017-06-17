from ... import share


async def on_ready():
    print("    Connected.\n"
          + "Ready.\n"
          + "---\n"
          + "To add this bot to a server, use this link:\n"
          + "{}\n".format(share.discord.utils.oauth_url(share.client_id))
          + "---")
