#!/usr/bin/env bash
set -o errexit  # Exit on error

# Install Node.js
apt-get update && apt-get install -y curl gnupg
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Python deps
pip install -r requirements.txt
