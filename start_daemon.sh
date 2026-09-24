#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-02-99845fbbae24
export GOOGLE_CLOUD_LOCATION=us-east4
export PORT=8080
export PATH="$HOME/.local/bin:$PATH"

PID=$(pgrep -f "python.*frontend/main.py" || true)
if [ -n "$PID" ]; then
    echo "Daemon is already running with PID $PID"
    exit 0
fi

nohup .venv/bin/python3 frontend/main.py > daemon.log 2>&1 &
NEW_PID=$!
echo "Started PlantCare Greenhouse web daemon service (PID $NEW_PID) on http://0.0.0.0:8080"
