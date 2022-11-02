#!/bin/sh
echo "Running launch script"
cd /home/pi/magic-paper
git pull
poetry run python magic_paper/main.py