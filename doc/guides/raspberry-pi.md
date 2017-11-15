# Raspberry Pi

## Basics

```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get clean
sudo apt-get autoclean
sudo raspi -config (for localisation and enable ssh)
use sudo bash (file) to run .sh scripts
use sudo nano (file) to edit text
```

## Install UI (optional)

```sh
sudo apt-get install --no-install-recommends xserver-xorg
sudo apt-get install --no-install-recommends xinit
sudo apt-get install raspberrypi-ui-mods
startx
```

## Install Apache

```sh
sudo apt-get install apache2 -y
sudo chown pi: /var/www/html
```

## Install Python

```sh
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
```

## ZLIB1G-DEV ALREADY INSTALLED SET TO MANUAL, MAYBE YOU SHOULDN'T REMOVE IT AT THE END

```sh
cd /usr/src
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz
tar xf Python-3.6.1.tar.xz
cd Python-3.6.1
sudo ./configure
sudo make -j4
sudo make altinstall
```

## Remove Build Tools

```sh
sudo rm -r Python-3.6.1
rm Python-3.6.1.tgz
sudo apt-get --purge remove build-essential tk-dev
sudo apt-get --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev
sudo apt-get --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
sudo apt-get --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
sudo apt-get autoremove
sudo apt-get clean
```

## Install Modis Requirements

```sh
sudo python3.6 -m pip install discord.py
sudo python3.6 -m pip install youtube-dl
sudo python3.6 -m pip install requests
sudo python3.6 -m pip install google-api-python-client
sudo apt-get install libsodium-dev libffi-dev
sudo python3.6 -m pip install pynacl
sudo apt-get install libxml2-dev libxslt-dev
sudo python3.6 -m pip install lxml
```

## Install FFmpeg

```sh
cd /usr/src
sudo git clone git://git.videolan.org/x264
cd x264
sudo ./configure --host=arm-unknown-linux-gnueabi --enable-static --disable-opencl
sudo make -j4
sudo make install
```

```sh
cd /usr/src
sudo git clone https://github.com/FFmpeg/FFmpeg.git
cd FFmpeg
sudo apt-get install libgnutls28-dev
sudo ./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree ***--enable-gnutls***
sudo make -j4
sudo make install
```
