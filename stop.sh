#!/bin/bash
cd "$(dirname "$0")"

if [ -f app.pid ] && kill -0 "$(cat app.pid)" 2>/dev/null; then
  kill "$(cat app.pid)"
  rm app.pid
  echo "Stopped."
else
  echo "App is not running."
  rm -f app.pid
fi
