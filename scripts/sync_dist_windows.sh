#!/usr/bin/env bash
# Refresh dist_windows from repo root (run before zipping for release).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DST="$ROOT/dist_windows"
mkdir -p "$DST"
cp "$ROOT/forward_channel_messages.py" "$ROOT/ui_app.py" "$ROOT/requirements.txt" "$DST/"
cp "$ROOT/.env.example" "$DST/env.example"
echo "Synced into $DST"
