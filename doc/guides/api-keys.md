---
title: API Keys
permalink: /guides/api-keys/
---
# Getting API Keys

API keys and tokens are needed for a few different parts of Modis. This guide should help guide you through creating those keys, and making sure Modis can use them.

## Making a Discord Bot

1. To get Modis running for Discord, first you need to create a bot. Head over to the [My Apps](https://discordapp.com/developers/applications/me) section of the Discord developer's page (if you aren't logged in to Discord you'll need to do that as well). ![My Apps](https://github.com/Infraxion/modis/raw/gh-pages/doc/guides/img/myapps.png?raw=true "My Apps")
1. Give your bot a name and an icon. This is what will appear in your server when you add it (you can change it at any time).
1. Select the 'Create App' button.
1. Scroll down and select 'Create a Bot User'. ![Create Bot User](https://github.com/Infraxion/modis/raw/gh-pages/doc/guides/img/createbotuser.png?raw=true "Create Bot User")

You now have your very own Discord Bot! You can add it to a server by putting your bot's client id in the [Discord Permissions Calculator](https://discordapi.com/permissions.html), and start Modis with your client id and bot token to have Modis running in your own server. For more details on setting up Modis, see the [Setup](./setup.md#modis-package) guide.

You can make you own bot invite link by pasting

```https
https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=2146958455
```

into your web browser and replacing `CLIENT_ID` with your bot's client id. You don't need to give all the permissions, but some modules won't work without the required permissions.

## Getting a Google API key

(Guide coming soon, feel free to ask for help in our Discord server)

## Making a SoundCloud application

Right now, SoundCloud have disabled making new applications. To use SoundCloud in Modis, you'll need to get a client id from an existing application, or wait until SoundCloud allow new applications again. We'll update this section with the new process for registering once SoundCloud have updated the process.
