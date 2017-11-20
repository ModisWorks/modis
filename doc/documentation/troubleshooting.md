---
title: Troubleshooting
permalink: /documentation/troubleshooting/
---

# Troubleshooting

## I get errors when starting Modis or sending any message

Make sure Modis is in your server. If it is, this can be caused by a few problems, but this is usually because one or more requirements for Modis are  not up to date. To fix this, run

```sh
pip3 install <packagename> --upgrade
```

or

```sh
pip3 uninstall <packagename>
pip3 install <packagename>
```

for each package listed in the `requirements.txt`.

## I get syntax errors when running Modis

If the syntax errors are in any of the Modis code (i.e. not the modules), then this is probably caused by Python. Make sure you are running the correct version of Python, and also try uninstalling and reinstalling Python.

## I get import errors when running Modis

This is either caused by not having the packages installed from `requirements.txt`, or the packages being installed to the wrong version of Python. When multiple versions of Python are installed on the same computer, run `pip3 install <packagename>` instead of `pip install <packagename>` to make sure that the packages are being installed for the right version of Python.

## The search function isn't working for the music module

You need to add your Google API key, either through the module UI or by adding `'google': '<YOUR_KEY>'` to the 'keys' section in your `data.json`. Your API key must have YouTube v3 enabled for Modis to work. If your Google API key has been added, make sure you have restarted Modis for the changes to take effect.

*We'll keep adding to this section as we find solutions to more problems you've found.*
