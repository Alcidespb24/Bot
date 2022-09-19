FROM python:3

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND noninteractive
ENV DISPLAY :2

#create App directory
RUN mkdir /app

# install wine for GUI
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt -yq install gnupg2 software-properties-common && \
    wget -nc https://dl.winehq.org/wine-builds/winehq.key && \
    apt-key add winehq.key && \
    apt-add-repository https://dl.winehq.org/wine-builds/debian/ && \
    apt update && \
    wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_11/Release.key | apt-key add -  && \  
    echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_11 ./" | tee /etc/apt/sources.list.d/wine-obs.list && \
    apt update -yq && apt install -yq --install-recommends winehq-stable && \
    apt-get -yq install xserver-xorg-video-dummy && \
    apt-get -y clean


# Copy Script
COPY ./src ./app

# install python dependencies 
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Copy helper Files
COPY ./Docker/ /root

# create wine prefix
RUN WINEPREFIX=/root/.wine WINARCH=x64 winecfg -v=win10


RUN unzip /root/Python.zip -d /root/Python && \
    mv /root/Python /root/.wine/drive_c/users/root/AppData/Local/Programs/ && \
    rm /root/Python.zip

#copy MetaTrader 5 installation
RUN unzip /root/MetaTrader\ 5.zip -d /root && \
    mv /root/MetaTrader\ 5 /root/.wine/drive_c/Program\ Files/ && \
    rm /root/MetaTrader\ 5.zip

#CMD ./root/init.sh
CMD /bin/bash ./root/init.sh
