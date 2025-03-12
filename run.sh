#!/bin/bash

source venv/bin/activate

# Get optional first argument if it exists; directory of video files
if [ -z "$1" ]; then
    echo "No argument provided. Running video web server with default argument."
    python index.py
else
    echo "Running video web server with argument: $1"
    python index.py $1
fi

