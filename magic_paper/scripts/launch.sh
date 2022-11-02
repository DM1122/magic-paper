#!/bin/sh
echo "Running launch script"
cd /home/pi/magic-paper
echo "Changed directory"
git pull
echo "Git pulled"
poetry run python magic_paper/main.py
echo "Ran Poetry"