#!/usr/bin/env bash
set -e

PID=$(pgrep -f "python.*frontend/main.py" || true)
if [ -n "$PID" ]; then
    echo "Stopping daemon process PID $PID..."
    kill -9 $PID
    echo "Stopped."
else
    echo "No running daemon process found."
fi
