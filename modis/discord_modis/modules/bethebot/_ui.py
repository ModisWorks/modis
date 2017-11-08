import asyncio as _asyncio
import logging
import tkinter as tk
from tkinter import ttk

from modis import datatools
from ._data import *
from ..._client import client

logger = logging.getLogger(__name__)


class ModuleUIFrame(ttk.Frame):
    """The UI for the bethebot module"""

    def __init__(self, parent):
        """The console tab for bethebot

        Args:
            parent: tk or ttk element
        """

        super(ModuleUIFrame, self).__init__(parent, padding=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        chat = ChatFrame(self)
        chat.grid(column=0, row=0, sticky="W E N S")


class ChatFrame(ttk.LabelFrame):
    """The chat frame for the BeTheBot module"""

    def __init__(self, parent):
        """Send messages from the bot

        Args:
            parent:
        """

        super(ChatFrame, self).__init__(parent, padding=8, text="Chat")

        self.channel = tk.StringVar()
        self.message = tk.StringVar()

        self.channel_frame = ttk.Frame(self)
        self.channel_frame.grid(column=0, row=0, sticky="W E")
        self.channel_label = ttk.Label(self.channel_frame, text="Channel ID:")
        self.channel_label.grid(column=0, row=0, sticky="W E")
        self.channel_box = ttk.Entry(self.channel_frame, textvariable=self.channel)
        self.channel_box.grid(column=0, row=1, sticky="W E")
        self.channel_frame.columnconfigure(0, weight=1)

        self.message_frame = ttk.Frame(self)
        self.message_frame.grid(column=0, row=1, pady=8, sticky="W E")
        self.message_label = ttk.Label(self.message_frame, text="Message:")
        self.message_label.grid(column=0, row=0, sticky="W E")
        self.message_box = ttk.Entry(self.message_frame, textvariable=self.message)
        self.message_box.grid(column=0, row=1, sticky="W E")
        self.message_frame.columnconfigure(0, weight=1)

        self.send_button = ttk.Button(self, command=lambda: self.add_current_message(), text="Send")
        self.send_button.grid(column=0, row=2, sticky="W")

        self.columnconfigure(0, weight=1)

    def add_current_message(self):
        """Adds a reaction with the current field options"""
        send_message(self.channel.get(), self.message.get())


def send_message(channel_id, message):
    """
    Send a message to a channel

    Args:
        channel_id (str): The id of the channel to send the message to
        message (str): The message to send to the channel
    """

    channel = client.get_channel(channel_id)

    if channel is None:
        logger.info("{} is not a channel".format(channel_id))
        return

    # Check that it's enabled in the server
    data = datatools.get_data()
    if not data["discord"]["servers"][channel.server.id][modulename]["activated"]:
        logger.info("This module has been disabled in {} ({})".format(channel.server.name, channel.server.id))

    try:
        runcoro(client.send_message(channel, message))
    except Exception as e:
        logger.exception(e)


def runcoro(async_function):
    """
    Runs an asynchronous function without needing to use await - useful for lambda

    Args:
        async_function (Coroutine): The asynchronous function to run
    """

    future = _asyncio.run_coroutine_threadsafe(async_function, client.loop)
    result = future.result()
    return result
