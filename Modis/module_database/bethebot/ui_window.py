from ...tools import ui_window
from ...share import *
import tkinter as tk
from tkinter import ttk

pagename = "bethebot"
pad_element = 2


class Page(ui_window.Page):
    def __init__(self, parent):
        """The console tab for bethebot

        Args:
            parent: tk or ttk element
        """

        super(Page, self).__init__(parent)

        chat = Chat(self)
        react = React(self)

        chat.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E"
        )
        react.grid(
            column=0,
            row=1,
            padx=pad_element,
            pady=pad_element,
            sticky="W E"
        )

        self.columnconfigure(0, weight=1)


class Chat(ui_window.Frame):
    def __init__(self, parent):
        """Send messages from the bot

        Args:
            parent:
        """

        super(Chat, self).__init__(parent, "Chat")

        self.channel = tk.StringVar()
        self.message = tk.StringVar()

        self.channel_label = ttk.Label(
            self,
            text="Channel ID:"
        )
        self.channel_box = ttk.Entry(
            self,
            textvariable=self.channel,
            width=18,
            font=("Courier", 9)
        )

        self.message_label = ttk.Label(
            self,
            text="Message:"
        )
        self.message_box = ttk.Entry(
            self,
            textvariable=self.message
        )
        self.send_button = ttk.Button(
            self,
            command=lambda: send_message(self.channel, self.message),
            text="Send"
        )

        self.channel_label.grid(
            column=0,
            row=1,
            padx=pad_element,
            pady=pad_element,
            sticky="E"
        )
        self.channel_box.grid(
            column=1,
            row=1,
            padx=pad_element,
            pady=pad_element,
            sticky="W"
        )
        self.message_label.grid(
            column=0,
            row=2,
            padx=pad_element,
            pady=pad_element,
            sticky="E"
        )
        self.message_box.grid(
            column=1,
            row=2,
            padx=pad_element,
            pady=pad_element,
            sticky="W E"
        )
        self.send_button.grid(
            column=1,
            row=3,
            padx=pad_element,
            pady=pad_element,
            sticky="W"
        )

        self.columnconfigure(1, weight=1)


class React(ui_window.Frame):
    def __init__(self, parent):
        """React to messages from the bot

        Args:
            parent: tk or ttk object
        """

        super(React, self).__init__(parent, "React™")

        self.channel = tk.StringVar()
        self.message = tk.StringVar()

        self.message_label = ttk.Label(
            self,
            text="Message ID:"
        )
        self.message_box = ttk.Entry(
            self,
            textvariable=self.channel,
            width=18,
            font=("Courier", 9)
        )

        self.emoji_label = ttk.Label(
            self,
            text="Emoji:"
        )
        self.emoji_box = ttk.Entry(
            self,
            textvariable=self.message,
            width=5
        )
        self.send_button = ttk.Button(
            self,
            command=lambda: add_reaction(self.channel, self.message),
            text="React™"
        )

        self.message_label.grid(
            column=0,
            row=1,
            padx=pad_element,
            pady=pad_element,
            sticky="E"
        )
        self.message_box.grid(
            column=1,
            row=1,
            padx=pad_element,
            pady=pad_element,
            sticky="W"
        )
        self.emoji_label.grid(
            column=0,
            row=2,
            padx=pad_element,
            pady=pad_element,
            sticky="E"
        )
        self.emoji_box.grid(
            column=1,
            row=2,
            padx=pad_element,
            pady=pad_element,
            sticky="W"
        )
        self.send_button.grid(
            column=1,
            row=3,
            padx=pad_element,
            pady=pad_element,
            sticky="W"
        )


def send_message(channel, message):
    try:
        runcoro(client.send_message(channel, message))
    except discord.DiscordException:
        pass


def add_reaction(message_id, emoji):
    message = client.get_message(message_id)
    try:
        runcoro(client.add_reaction(message, emoji))
    except discord.DiscordException:
        pass


def valid_channel_id(id_string):
    if len(id_string) == 18:
        try:
            int(id_string)
        except TypeError:
            return False
        else:
            return True
    else:
        return False
