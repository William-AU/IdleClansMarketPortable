#!/bin/sh

VERSION_FILE="VERSION"

CURRENT_VERSION=""

while :
do
  echo "Looking for update..."
  git fetch

  REMOTE_HASH=$(git rev-parse origin/$(git rev-parse --abbrev-ref HEAD))
  LOCAL_HASH=$(git rev-parse HEAD)

  if [ "$REMOTE_HASH" != "$LOCAL_HASH" ]; then
    echo "Update available! Pulling changes..."
    git stash push -m "temp" autostart.sh
    git pull
    git stash pop

    if [ -f "$VERSION_FILE" ]; then
      NEW_VERSION=$(cat "$VERSION_FILE")
      if [ "$NEW_VERSION" != "$CURRENT_VERSION" ]; then
        echo "Version updated: $CURRENT_VERSION → $NEW_VERSION"
        CURRENT_VERSION=$NEW_VERSION

        # Kill any old main.py process
        PID=$(pgrep -f "python.*main.py")
        if [ -n "$PID" ]; then
          echo "Stopping old main.py (PID $PID)..."
          kill $PID
        fi

        # Start new main.py in background
        echo "Starting new main.py..."
        nohup python3 main.py > main.log 2>&1 &
      fi
    fi
  else
    echo "No update available."
  fi

  sleep 20m
done