# Troubleshooting

## My data.json has no servers in it, even though Modis is in my server

This is usually because one or more requirements for Modis are installed, but not up to date. To fix this, run `pip install [packagename] --update`, or `pip uninstall` and then `pip reinstall` each package.

## The search function isn't working for the music module

You need to add your Google API key, either through the module UI or by adding `'google': '<YOUR_KEY>'` to the 'keys' section in your `data.json`. Your API key must have YouTube v3 enabled for Modis to work.

*We'll keep adding to this section as we find solutions to more problems you've found.*
