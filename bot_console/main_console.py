import tkinter as tk
import asyncio

client = None
window_name = "Discord Console"
pad_frame = 4
pad_element = 2


class RootFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(RootFrame, self).__init__(
            parent,
            **kwargs
        )

        self.title = tk.Label(
            self,
            text="-------- " + window_name + " --------"
        )

        self.chat_frame = ChatFrame(self)

        self.title.grid(
            column=0,
            row=0,
            padx=pad_frame,
            pady=pad_frame
        )
        self.chat_frame.grid(
            column=0,
            row=1,
            padx=pad_frame,
            pady=pad_frame
        )


class ChatFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(ChatFrame, self).__init__(
            parent,
            relief='groove',
            bd=2,
            padx=pad_element,
            pady=pad_element,
            **kwargs
        )

        self.channel = tk.StringVar()
        self.message = tk.StringVar()

        self.title = tk.Label(
            self,
            text="-------- Chat --------"
        )

        self.channel_label = tk.Label(
            self,
            text="Channel ID:"
        )
        self.channel_box = tk.Entry(
            self,
            textvariable=self.channel,
            width=18,
            font=("Source Code Pro", 9)
        )

        self.message_label = tk.Label(
            self,
            text="Message:"
        )
        self.message_box = tk.Entry(
            self,
            textvariable=self.message,
            width=64
        )
        self.send_button = tk.Button(
            self,
            command=lambda: runcoro(say(self.channel, self.message)),
            text="Send"
        )

        self.title.grid(
            column=0,
            row=0,
            columnspan=2,
            padx=pad_element,
            pady=pad_element
        )
        self.channel_label.grid(
            column=0,
            row=1,
            padx=pad_element,
            pady=pad_element,
            sticky=tk.E
        )
        self.channel_box.grid(
            column=1,
            row=1,
            padx=pad_element,
            pady=pad_element,
            sticky=tk.W
        )
        self.message_label.grid(
            column=0,
            row=2,
            padx=pad_element,
            pady=pad_element,
            sticky=tk.E
        )
        self.message_box.grid(
            column=1,
            row=2,
            padx=pad_element,
            pady=pad_element)
        self.send_button.grid(
            column=1,
            row=3,
            padx=pad_element,
            pady=pad_element,
            sticky=tk.W
        )

    def valid_channel_id(self, id_string):
        if len(id_string) == 18:
            try:
                int(id_string)
            except TypeError:
                return False
            else:
                return True
        else:
            return False


def init(iclient, name):
    print("Loading console...")

    global client
    client = iclient
    global window_name
    window_name = name


def main():
    window = tk.Tk()
    window.title(window_name)

    root_frame = RootFrame(window)
    root_frame.grid(
        padx=1,
        pady=1
    )

    window.mainloop()


def runcoro(async_function):
    asyncio.run_coroutine_threadsafe(async_function, client.loop)


async def say(channel, message):
    await client.send_message(client.get_channel(str(channel.get())), content=str(message.get()))
