#!/bin/bash

set -e

echo "---------------------------------"
echo "-------- setup wine prefix ------"
echo "---------------------------------"
# We need the developer version of wine.  We need at least version 4.14 (see link).
# This is the earliest version I've seen reported to work with python3 well
# Without this, we'd have to run the embedded install of python which is riddled
# with annoying issues.

# see: https://appdb.winehq.org/objectManager.php?sClass=version&iId=38187

echo "------ Installing required apt packages ------"
apt update
apt install -y wget gnupg software-properties-common apt-utils

echo "------ Downloading Gecko Package -----"
wget -P ~/.cache/wine/ http://dl.winehq.org/wine/wine-gecko/2.47.2/wine-gecko-2.47.2-x86_64.msi
wget -P ~/.cache/wine/ http://dl.winehq.org/wine/wine-gecko/2.47.2/wine-gecko-2.47.2-x86.msi

echo "------- Adding contib repo -------"
apt-add-repository  'deb http://deb.debian.org/debian bullseye main contrib non-free'

echo "------ Add latest wine repo ------"
# Need at least wine 4.14 to install python 3.7
dpkg --add-architecture i386
wget -nc https://dl.winehq.org/wine-builds/winehq.key
apt-key add winehq.key
apt-add-repository 'deb https://dl.winehq.org/wine-builds/debian/ bullseye main'
apt update

# Add repo for faudio package.  Required for winedev
add-apt-repository -y ppa:cybermax-dexter/sdl2-backport

echo "-------- Install wine-dev ------"

apt install -y \
    winehq-devel \
    winetricks \
    winbind \
    xvfb        # This is for making a dummy X server disply 

echo "------ Download python ------"
wget -P /root/ https://www.python.org/ftp/python/3.10.7/python-3.10.7-amd64.exe

echo "------ Init wine prefix ------"
WINEPREFIX=~/.wine WINARCH=win64 winetricks \
    win10

# Setup dummy screen
Xvfb :0 -screen 0 1024x768x16 &
jid=$!

echo "------ Install python ------"
DISPLAY=:0.0 WINEPREFIX=~/.wine wine cmd /c \
    /root/python-3.10.7-amd64.exe \
    /quiet \
    PrependPath=1 \
    && echo "Python Installation complete!"

echo "----- Install windows python dependencies ------"
WINEPREFIX=~/.wine wine cmd /c ~/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python310/Scripts/pip.exe install rpyc MetaTrader5

echo "---- Cleaning up.... -----"
apt-get -y remove xvfb 
apt-get -y clean

# Display=:0.0 redirects wine graphical output to the dummy display.  
# This is to avoid docker errors as the python installer requires a display, 
# even when quiet install is specified.
