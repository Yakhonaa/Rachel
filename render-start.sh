#!/usr/bin/env bash
set -euo pipefail

echo "=== start: verify node available ==="
which node || true
node -v || true

echo "=== starting bot ==="
# Unbuffered python output so logs appear live
exec python -u main.py
