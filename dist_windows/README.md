# Telegram channel forwarder — Windows package

Portable folder: copy this entire `dist_windows` directory to any Windows PC with **Python 3.10+** installed.

## Quick start

1. **Double-click `START.bat`** (or run `python windows_launcher.py` in Command Prompt from this folder).
2. First run: a **`venv`** folder is created and dependencies install from `requirements.txt`.
3. If `.env` is missing, it is created from **`env.example`** — edit **`.env`** with your [my.telegram.org](https://my.telegram.org) API ID/hash and at least `TELEGRAM_FORWARD_TO_1` + `TELEGRAM_KEYWORDS_1`.
4. Use the menu:
   - **1** — Run the forwarder (long-running; leave the window open or use Task Scheduler — see below).
   - **2** — Run the local web UI at [http://127.0.0.1:8765](http://127.0.0.1:8765).

## Requirements

- Windows 10/11 (or Windows Server) with **Python 3** on `PATH` (`python` / `py` launcher).
- Internet on first run (pip install).

## What’s included

| File | Purpose |
|------|--------|
| `windows_launcher.py` | Creates `venv`, installs deps, menu |
| `forward_channel_messages.py` | Main Telethon forwarder |
| `ui_app.py` | Flask UI for `logs/forwards.jsonl` + sound mute |
| `requirements.txt` | telethon, python-dotenv, flask |
| `env.example` | Template for `.env` |

Session files and logs are written **next to these files** (`logs/`, `*.session`).

## Sounds

The forwarder uses **macOS `afplay`** when `TELEGRAM_PLAY_SOUND_*` is enabled. On Windows, those flags are ignored (no crash). Use the web UI for monitoring; optional Windows sound support would require a separate change.

## Run forwarder in the background (Windows)

Use **Task Scheduler** to run at logon, for example:

- Program: `C:\Path\To\dist_windows\venv\Scripts\python.exe`
- Arguments: `forward_channel_messages.py`
- Start in: `C:\Path\To\dist_windows`

Or run `python forward_channel_messages.py` in a minimized window.

## Updating from the main repo

If you develop in the parent project, refresh the copies in this folder:

```bash
# From repo root (macOS/Linux)
./scripts/sync_dist_windows.sh
```

Then re-zip `dist_windows` for distribution.

## Troubleshooting

- **`python` not found** — Install Python from [python.org](https://www.python.org/downloads/) and check “Add Python to PATH”.
- **First login** — Telethon will ask for phone and code in the console when you start the forwarder.
- **Firewall** — Allow Python if prompted; the UI only binds to `127.0.0.1`.
