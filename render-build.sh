#!/usr/bin/env bash
set -o errexit  # Exit on error

# Install Python deps
pip install -r requirements.txt

# Install Node.js inside the Python venv
nodeenv -p --node=18.16.0

