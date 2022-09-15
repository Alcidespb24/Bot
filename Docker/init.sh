#!/bin/bash

Xorg -noreset +extension GLX +extension RANDR +extension RENDER -config /root/xorg.conf :2 &

python -m mt5linux /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python310/python.exe