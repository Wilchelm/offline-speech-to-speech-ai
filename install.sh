#!/bin/bash
set -e

# Get absolute path of the script directory
SCRIPT_DIR=$(cd "$(dirname "$0")" &>/dev/null && pwd)

echo "--- Starting Installation (Ubuntu) ---"

# 1. Install system dependencies
echo "Installing system dependencies (this may take a moment)..."
sudo apt update
sudo apt install -y build-essential python3-dev python3-venv portaudio19-dev libportaudio2 libasound2-dev cmake

# 2. Create virtual environment
if [ -d "env" ]; then
    echo "Existing 'env' directory found. Removing to ensure a clean setup..."
    rm -rf env
fi

echo "Creating virtual environment..."
python3 -m venv env

mkdir -p models

# 3. Install Python packages
echo "Installing Python packages from requirements.txt..."
"$SCRIPT_DIR/env/bin/python3" -m pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    "$SCRIPT_DIR/env/bin/python3" -m pip install -r requirements.txt
else
    echo "Error: requirements.txt not found!"
    exit 1
fi

echo "--- Installation Completed Successfully! ---"
echo "To run the project, use: ./run.sh"
