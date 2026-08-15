#!/bin/bash

# Get absolute path of the script directory
SCRIPT_DIR=$(cd "$(dirname "$0")" &>/dev/null && pwd)

# Run the script using the interpreter from the virtual environment
"$SCRIPT_DIR/env/bin/python3" "$SCRIPT_DIR/speech_to_speech_ai.py" "$@"
