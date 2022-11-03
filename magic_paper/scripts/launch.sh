#!/bin/sh
echo "Running launch script"

echo "Current directory: $PWD. Changing directory..."
cd /home/pi/magic-paper
echo "Changed directory to: $PWD"

echo "Pulling git..."
git pull

echo "Running python script..."
/home/pi/.local/bin/poetry run python magic_paper/main.py

echo "Done!"