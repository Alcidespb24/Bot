#!/bin/bash

IS_MT5_RUNNING=`pgrep python`
MT5_TEMP_DIR="/tmp/mt5linux"
IS_XORG_RUNNING=`pgrep Xorg`
META_QUOTES_DIR="/root/.wine/drive_c/users/root/AppData/Roaming/MetaQuotes"
NUMBER_OF_ATTEMPTS=3

XORG_FILE="/usr/share/X11/xorg.conf.d"
XORG_LOCK_FILE="/tmp/.X2-lock"

if ! [ -d "/app" ]; then
    echo "APP Volume not mounted....."
    echo "Please Run the contianer with -v /path/in/local/machine/to/app:/app"
    exit 1
fi

function cleanEnv() 
{
    echo "Exiting...."
    echo "Killing Xorg..."
    pgrep Xorg | xargs kill
    if [ -d "$XORG_FILE" ]; then
        rm -rf "$XORG_FILE"
    fi

    if [ -f "$XORG_LOCK_FILE" ]; then
        rm "$XORG_LOCK_FILE"
    fi
       
    echo "Killing wine and python..."
    wineserver -k9
    rm -rf /tmp/*

    if [ -d "$META_QUOTES_DIR" ]; then
        rm -rf /root/.wine/drive_c/users/root/AppData/Roaming/MetaQuotes
    fi 

    if ! [ -z "$MT5LINUX_PID"  ]; then
        kill "$MT5LINUX_PID"    
    fi

    pkill python
    wait
}

function startXorg()
{
    Xorg -noreset +extension GLX +extension RANDR +extension RENDER -config /root/xorg.conf :2 &
}

function startMt5Server()
{
    DISPLAY=:2 WINEDLLOVERRIDES=mscoree=d;mshtml=d python -m mt5linux -w wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python310/python.exe >/dev/null & 
    MT5LINUX_PID="$$"
}

function areWeReadyToRun()
{
    iterationCounter=0
    while ! [[ "$SERVER_STATUS" == *"succeeded!"* || "$SERVER_STATUS" == *"Connected"* ]]
    do
        if [ $iterationCounter -eq 30 ]; then
            break;
            return 1
        fi
        iterationCounter=$(($iterationCounter+1))
        SERVER_STATUS=`nc -zv 127.0.0.1 18812 2>&1`
        echo "Waiting for mt5linux server....."
        echo "$SERVER_STATUS"
        sleep 2s
    done

    return 0
}

function runApp()
{
    DISPLAY=:2 wine ~/.wine/drive_c/Program\ Files/MetaTrader\ 5/terminal64.exe /config:c:\defaultInitDemo.ini &

    DISPLAY=:2 WINEDLLOVERRIDES=mshtml= python /app/main.py
}

trap cleanEnv SIGINT
trap cleanEnv SIGKILL

attemptsCounter=1
while ! [[ $attemptsCounter -eq $NUMBER_OF_ATTEMPTS ]]
do
    cleanEnv

    startXorg

    startMt5Server

    if areWeReadyToRun 
    then
        break
    else
        if [ $attemptsCounter -eq $NUMBER_OF_ATTEMPTS ]; then
            exit 1
        fi
        attemptsCounter=$(($attemptsCounter+1))
    fi
done


runApp