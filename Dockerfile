FROM python:3

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND noninteractive
ENV DISPLAY :2

#create App directory
RUN mkdir /app

# Copy Script
COPY ./src ./app

RUN apt update && \ 
    apt-get -yq install xserver-xorg-video-dummy ncat

# install python dependencies 
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Copy helper Files
COPY ./Docker/ /root

#install python and wine
RUN chmod u+x /root/installPython.sh && \
    ./root/installPython.sh

#copy MetaTrader 5 installation
RUN unzip /root/MetaTrader\ 5.zip -d /root && \
    mv /root/MetaTrader\ 5 /root/.wine/drive_c/Program\ Files/ && \
    rm /root/MetaTrader\ 5.zip
    

#CMD ./root/init.sh
CMD /bin/bash ./root/init.sh
