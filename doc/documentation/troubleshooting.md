---
title: Troubleshooting
permalink: /documentation/troubleshooting/
---

# Troubleshooting

## I get errors when starting Modis or sending any message

Make sure Modis is in your server. If it is, this can be caused by a few problems, but this is usually because one or more requirements for Modis are  not up to date. To fix this, run

```sh
pip install [packagename] --upgrade
```

or

```sh
pip uninstall [packagename]
pip install [packagename]
```

for each package listed in the `requirements.txt`.

## I get syntax errors when running Modis

If the syntax errors are in any of the Modis code (i.e. not the modules), then this is probably caused by Python. Make sure you are running the correct version of Python, and also try uninstalling and reinstalling Python.

## The search function isn't working for the music module

You need to add your Google API key, either through the module UI or by adding `'google': '<YOUR_KEY>'` to the 'keys' section in your `data.json`. Your API key must have YouTube v3 enabled for Modis to work. If your Google API key has been added, make sure you have restarted Modis for the changes to take effect.

*We'll keep adding to this section as we find solutions to more problems you've found.*
