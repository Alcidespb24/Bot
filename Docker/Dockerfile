FROM python:3

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND noninteractive

#create App directory
RUN mkdir /app

# install win and intel drivers for GUI
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get -yq install libgl1-mesa-glx libgl1-mesa-dri && \
    apt -yq install gnupg2 software-properties-common && \
    wget -nc https://dl.winehq.org/wine-builds/winehq.key && \
    apt-key add winehq.key && \
    apt-add-repository https://dl.winehq.org/wine-builds/debian/ && \
    apt update && \
    wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_11/Release.key | apt-key add -  && \  
    echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_11 ./" | tee /etc/apt/sources.list.d/wine-obs.list && \
    apt update -yq && apt install -yq --install-recommends winehq-stable
    

COPY . .
# # install dependencies 
# COPY requirements.txt ./app
# RUN pip install --no-cache-dir -r ./app/requirements.txt


# Create wine prefix
RUN WINEPREFIX=/root/.wine WINEARCH=win64 DISPLAY= wine "python-3.10.6-amd64.exe /quiet"



CMD [ "wine", "--version" ]