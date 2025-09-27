#!/usr/bin/env bash
set -euo pipefail

echo "=== build: upgrade pip, install python deps ==="
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "=== ensure nodeenv installed ==="
python -m pip install --upgrade nodeenv

echo "=== inject Node.js into the current venv ==="
# -p modifies the current Python venv (Render uses a virtualenv for build/run),
# so node will be available in runtime as well.
nodeenv -p --node=18.16.0

echo "=== sanity checks: show node path and version ==="
python - <<'PY'
import shutil, subprocess,sys
print("which node:", shutil.which("node"))
try:
    print("node -v:", subprocess.check_output(["node","-v"], text=True).strip())
except Exception as e:
    print("node -v error:", e)
PY

echo "=== build finished ==="
