from ..._client import client


async def on_message(message):
    # Check the content of the message
    if message.content == "ping":
        # Respond with 'ping'
        await client.send_typing(message.channel)
        await client.send_message(message.channel, "pong")
