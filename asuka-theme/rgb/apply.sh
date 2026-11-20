#!/usr/bin/env bash
# Применить NERV/Eva-02 узор к клавиатуре: временный OpenRGB-сервер -> скрипт -> стоп.
R=$HOME/.local/share/asuka-theme/rgb
"$HOME/Applications/OpenRGB.AppImage" --server --noautoconnect > "$R/server.log" 2>&1 &
PID=$!
for _ in $(seq 1 30); do (echo > /dev/tcp/127.0.0.1/6742) 2>/dev/null && break; sleep 1; done
"$R/venv/bin/python" "$R/asuka_kbd.py"
kill "$PID" 2>/dev/null
