---
title: Troubleshooting
permalink: /documentation/troubleshooting/
---

# Troubleshooting

## How do I get Modis in my server?

[Discord Permissions Calculator](https://discordapi.com/permissions.html) will generate an invite link for you, or you can make you own by using `https://discordapp.com/oauth2/authorize?client_id=<CLIENT_ID>&scope=bot&permissions=2146958455` and replacing `<CLIENT_ID>` with your bot's client id. You don't need to give all the permissions, but some modules won't work without the required permissions.

## My data.json has no servers in it

Make sure Modis is in your server. If it is, then this is usually because one or more requirements for Modis are installed, but not up to date. To fix this, run `pip install [packagename] --update`, or `pip uninstall` and then `pip uninstall` each package. Make sure to run `pip install discord.py` 

## The search function isn't working for the music module

You need to add your Google API key, either through the module UI or by adding `'google': '<YOUR_KEY>'` to the 'keys' section in your `data.json`. Your API key must have YouTube v3 enabled for Modis to work. If your Google API key has been added, make sure you have restarted Modis for the changes to take effect.

*We'll keep adding to this section as we find solutions to more problems you've found.*
