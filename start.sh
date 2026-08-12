#!/bin/bash
cd "$(dirname "$0")"

if [ -f app.pid ] && kill -0 "$(cat app.pid)" 2>/dev/null; then
  echo "App already running (PID $(cat app.pid)) - http://localhost:5050"
  exit 0
fi

source venv/Scripts/activate
nohup python app.py > app.log 2>&1 &
echo $! > app.pid
sleep 1
echo "Started at http://localhost:5050 (PID $(cat app.pid))"
echo "Logs: tail -f $(pwd)/app.log"
echo "Stop: ./stop.sh"
