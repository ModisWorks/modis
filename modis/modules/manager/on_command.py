import logging

from modis import main
from modis.tools import data

from . import api_manager, ui_embed

logger = logging.getLogger(__name__)


async def on_command(root, aux, query, msgobj):
    is_admin = msgobj.author == msgobj.server.owner
    for role in msgobj.author.roles:
        if role.permissions.administrator:
            is_admin = True
            break

    if not is_admin:
        await main.client.send_typing(msgobj.channel)
        reason = "You must have a role that has the permission 'Administrator'"
        embed = ui_embed.error(msgobj.channel, "Insufficient Permissions", reason)
        await embed.send()
        return

    if root == "prefix" and query:
        await main.client.send_typing(msgobj.channel)
        new_prefix = query.replace(" ", "").strip()
        data.cache["servers"][msgobj.server.id]["prefix"] = new_prefix
        data.write()

        embed = ui_embed.modify_prefix(msgobj.channel, new_prefix)
        await embed.send()

    if root == "warnmax" and query:
        try:
            warn_max = int(query)
            if warn_max > 0:
                await main.client.send_typing(msgobj.channel)
                data.cache["servers"][msgobj.server.id]["manager"]["warnings_max"] = warn_max
                data.write()
                embed = ui_embed.warning_max_changed(msgobj.channel, warn_max)
                await embed.send()
            else:
                await main.client.send_typing(msgobj.channel)
                reason = "Maximum warnings must be greater than 0"
                embed = ui_embed.error(msgobj.channel, "Error", reason)
                await embed.send()
        except ValueError:
            await main.client.send_typing(msgobj.channel)
            reason = "Warning maximum must be a number"
            embed = ui_embed.error(msgobj.channel, "Error", reason)
            await embed.send()

    if root == "warn" and query:
        for user in msgobj.mentions:
            await api_manager.warn_user(msgobj.channel, user)

    if root == "ban" and query:
        for user in msgobj.mentions:
            await api_manager.ban_user(msgobj.channel, user)

    # TODO implement new module activation in core
    # if root == "activate" and query:
    #     await api_manager.activate_module(msgobj.channel, query, True)
    #
    # if root == "deactivate" and query:
    #     await api_manager.activate_module(msgobj.channel, query, False)
