# Dubai War Alerts by slumcap – Telegram Channel Forwarder

Forwards Telegram messages from **channels only** (ignores chats and groups) when they contain certain keywords.

## Prerequisites

- Python 3.8+
- A Telegram account (user, not bot)
- API credentials from [my.telegram.org](https://my.telegram.org)

## Setup

1. **Create an app** at [my.telegram.org](https://my.telegram.org) → API development tools.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment** – copy `.env.example` to `.env` and edit, or export:
   ```bash
   cp .env.example .env   # then edit .env
   # OR export directly:
   export TELEGRAM_API_ID=12345678
   export TELEGRAM_API_HASH=your_api_hash
   export TELEGRAM_FORWARD_TO=@your_username  # or chat ID / invite link
   export TELEGRAM_KEYWORDS=dubai,alert,urgent
   ```

## Run

```bash
python forward_channel_messages.py
```

On first run you’ll be asked for your phone number and the login code sent to Telegram.

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_API_ID` | Yes | From my.telegram.org |
| `TELEGRAM_API_HASH` | Yes | From my.telegram.org |
| `TELEGRAM_FORWARD_TO` | Yes | Username (`@user`), chat ID, or invite link |
| `TELEGRAM_KEYWORDS` | Yes | Comma-separated keywords (word-boundary match) |
| `TELEGRAM_SESSION` | No | Session file name (default: `dubai_alerts_session`) |
| `TELEGRAM_CASE_INSENSITIVE` | No | `true` or `false` (default: `true`) |

## Notes

- Only **broadcast channels** are processed; groups and private chats are ignored.
- You must be a member of the channels you want to monitor.
- Keywords use word boundaries (e.g. `dubai` does not match `dubaiairport`).
