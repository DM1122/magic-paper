#!/bin/sh
echo "Running launch script"
cd ~/magic-paper
echo "Changed directory"
git pull
echo "Git pulled"
poetry run python magic_paper/main.py
echo "Ran poetry"