#!/usr/bin/env python3
"""
Forward Telegram channel messages that contain certain keywords.

Only processes messages from broadcast channels (ignores chats and groups).
Requires user account credentials (API ID, API Hash from my.telegram.org).
"""

import asyncio
import os
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from telethon import TelegramClient, events
from telethon.tl.types import Channel

# Configuration via environment variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
API_ID = int(os.environ.get("TELEGRAM_API_ID", "0"))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
SESSION_NAME = os.environ.get("TELEGRAM_SESSION", "dubai_alerts_session")
SESSION_PATH = os.path.join(SCRIPT_DIR, SESSION_NAME)
FORWARD_TO = os.environ.get("TELEGRAM_FORWARD_TO", "")  # Username, ID, or invite link
KEYWORDS = os.environ.get("TELEGRAM_KEYWORDS", "dubai,alert,urgent").lower().split(",")
KEYWORDS = [k.strip() for k in KEYWORDS if k.strip()]

# Set to True for case-insensitive matching
KEYWORDS_CASE_INSENSITIVE = os.environ.get("TELEGRAM_CASE_INSENSITIVE", "true").lower() == "true"


def message_contains_keywords(text: str) -> bool:
    """Check if message text contains any of the configured keywords."""
    if not text:
        return False
    search_text = text.lower() if KEYWORDS_CASE_INSENSITIVE else text
    for keyword in KEYWORDS:
        # Word boundary match to avoid partial matches (e.g. "dubai" not matching "dubaiairport")
        pattern = rf"\b{re.escape(keyword.strip())}\b"
        if re.search(pattern, search_text, re.IGNORECASE if KEYWORDS_CASE_INSENSITIVE else 0):
            return True
    return False


async def main():
    print("Connecting to Telegram...", flush=True)
    if not API_ID or not API_HASH:
        print("Error: Set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables.", flush=True)
        print("Get them from https://my.telegram.org", flush=True)
        return
    if not FORWARD_TO:
        print("Error: Set TELEGRAM_FORWARD_TO (username, ID, or invite link of destination).", flush=True)
        return
    if not KEYWORDS:
        print("Error: Set TELEGRAM_KEYWORDS (comma-separated list of words to match).", flush=True)
        return

    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

    @client.on(events.NewMessage)
    async def handler(event):
        # Ignore outgoing messages (our own)
        if event.out:
            return

        chat = await event.get_chat()
        # Only process broadcast channels (not groups, not private chats)
        if not isinstance(chat, Channel) or not getattr(chat, "broadcast", False):
            return

        text = event.text or ""
        if not message_contains_keywords(text):
            return

        try:
            await event.forward_to(FORWARD_TO)
            print(f"Forwarded from {chat.title}: {text[:80]}...", flush=True)
        except Exception as e:
            print(f"Failed to forward: {e}", flush=True)

    await client.start()
    print(f"Listening for channel messages containing: {KEYWORDS}", flush=True)
    print(f"Forwarding to: {FORWARD_TO}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
