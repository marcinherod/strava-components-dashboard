#!/bin/bash
cd "$(dirname "$0")"

if [ -f app.pid ] && kill -0 "$(cat app.pid)" 2>/dev/null; then
  kill "$(cat app.pid)"
  rm app.pid
  echo "Zatrzymano."
else
  echo "Aplikacja nie działa."
  rm -f app.pid
fi
