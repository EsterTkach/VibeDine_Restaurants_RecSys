#!/bin/bash

echo "==================================="
echo " Launching VibeDine"
echo "==================================="

# Check Docker
if ! docker info >/dev/null 2>&1; then
    echo "Docker Desktop is not running."
    exit 1
fi

echo "Building and starting containers..."
docker compose up --build -d

echo
echo "Opening frontend..."
open http://localhost:5173

echo
echo "Streaming logs..."
docker compose logs -f