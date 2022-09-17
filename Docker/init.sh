#!/bin/bash

Xorg -noreset +extension GLX +extension RANDR +extension RENDER -config /root/xorg.conf :2 &

sleep 5s

DISPLAY=:2 python -m mt5linux -w wine64 /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python310/python.exe > /dev/null & 

sleep 15s

DISPLAY=:2 python /app/main.py