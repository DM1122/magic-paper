#!/bin/sh
echo "Running magic paper launch script"

echo "Current directory: '$PWD'. Changing directory..."
cd /home/pi/magic-paper
echo "Changed directory to: '$PWD'"

echo "Updating codebase..."
git pull

echo "Running script..."
/home/pi/.local/bin/poetry run python magic_paper/main.py

echo "Done!"