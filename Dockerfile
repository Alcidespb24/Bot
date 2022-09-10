FROM python:3

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND noninteractive

#create App directory
RUN mkdir /app

# install win and intel drivers for GUI
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt -yq install gnupg2 software-properties-common && \
    wget -nc https://dl.winehq.org/wine-builds/winehq.key && \
    apt-key add winehq.key && \
    apt-add-repository https://dl.winehq.org/wine-builds/debian/ && \
    apt update && \
    wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_11/Release.key | apt-key add -  && \  
    echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_11 ./" | tee /etc/apt/sources.list.d/wine-obs.list && \
    apt update -yq && apt install -yq --install-recommends winehq-stable

# copy wine config
COPY ./Docker/wineStuff/.wine ./root/.wine

# install dependencies 
COPY ./Docker/requirements.txt ./app
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Copy Script
COPY ./MainStrategy_MACD.py ./app

# run mt5 server
CMD [ "python","-m","mt5linux","/root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python310/python.exe"]