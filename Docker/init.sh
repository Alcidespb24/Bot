#!/bin/bash

IS_MT5_RUNNING=`pgrep python`
IS_XORG_RUNNING=`pgrep Xorg`

XORG_FILE="/usr/share/X11/xorg.conf.d"
XORG_LOCK_FILE="/tmp/.X2-lock"

if ! [ -z "$IS_XORG_RUNNING" ] ; then
    echo "Killing Xorg..."
    pgrep Xorg | xargs kill
    rm -rf "$XORG_FILE"   
    rm "$XORG_LOCK_FILE"

else
    if [ -d "$XORG_FILE"  ] ; then
        rm -rf "$XORG_FILE"       
    fi

    if [ -f "$XORG_LOCK_FILE" ] ; then
         rm "$XORG_LOCK_FILE"
    fi
fi
sleep 2s
Xorg -noreset +extension GLX +extension RANDR +extension RENDER -config /root/xorg.conf :2 &

if ! [ -z "$IS_MT5_RUNNING" ] ; then
    echo "Killing wine and python..."
    `pgrep python | xargs kill`
    `pgrep start.exe | xargs kill`
    `pgrep wine | xargs kill`
    `pgrep terminal | xargs kill`
    `pgrep -f windows | xargs kill`
    `wineserver -k9`
fi

DISPLAY=:2 python -m mt5linux -w wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python310/python.exe >/dev/null & 

while ! [[ "$SERVER_STATUS" == *"succeeded!"* || "$SERVER_STATUS" == *"Connected"* ]]
do
    SERVER_STATUS=`nc -zv 127.0.0.1 18812 2>&1`
    echo "Waiting for mt5linux server....."
    echo "$SERVER_STATUS"
    sleep 2s
done

kill "$(pgrep ncat)"

DISPLAY=:2 python /app/main.py