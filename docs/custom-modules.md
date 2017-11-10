# Custom Modules
In this guide you will learn, step by step, how to make a basic 'ping pong' module for Modis.

After completing this you will know how to:
* Set up a message receiver
* Send messages to Discord
* Listen for commands
* Create a `help.json` file for a module
* Activate and deactivate your module
* Use Modis' embed features


## Making a new module
Modis looks in the `modis\discord-modis\modules\` folder for Discord modules. To start making our module, make a new folder there called `pingpong`.

![Module folder structure](./img/pingpongfolder.png?raw=true "Module folder structure")


## Listening for messages
To listen to Discord events, a module needs a file with the name of the event. For a message, the file should be called `on_message.py` (a full list of Discord events can be found on the [events page](./events.md)).
