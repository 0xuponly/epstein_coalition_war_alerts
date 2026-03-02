#!/usr/bin/env python3
"""
Forward Telegram channel messages that contain certain keywords.

Only processes messages from broadcast channels (ignores chats and groups).
Requires user account credentials (API ID, API Hash from my.telegram.org).
"""

import asyncio
import os
import re
from typing import List, Tuple

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
SESSION_NAME = os.environ.get("TELEGRAM_SESSION", "epstein_coalition_alerts_session")
SESSION_PATH = os.path.join(SCRIPT_DIR, SESSION_NAME)

# Output channels: list of (destination, keywords_list)
# Channel 1: FORWARD_TO_1 + KEYWORDS_1, or legacy FORWARD_TO + KEYWORDS
# Channel 2: FORWARD_TO_2 + KEYWORDS_2
def _parse_keywords(s: str) -> List[str]:
    return [k.strip() for k in (s or "").lower().split(",") if k.strip()]


def _get_output_channels() -> List[Tuple[str, List[str]]]:
    channels = []
    # Channel 1
    dest1 = os.environ.get("TELEGRAM_FORWARD_TO_1")
    kw1 = _parse_keywords(
        os.environ.get("TELEGRAM_KEYWORDS_1") 
    )
    if dest1 and kw1:
        channels.append((dest1, kw1))
    # Channel 2
    dest2 = os.environ.get("TELEGRAM_FORWARD_TO_2")
    kw2 = _parse_keywords(os.environ.get("TELEGRAM_KEYWORDS_2", ""))
    if dest2 and kw2:
        channels.append((dest2, kw2))
    return channels

# Set to True for case-insensitive matching
KEYWORDS_CASE_INSENSITIVE = os.environ.get("TELEGRAM_CASE_INSENSITIVE", "true").lower() == "true"


def message_contains_keywords(text: str, keywords: List[str]) -> bool:
    """Check if message text contains any of the given keywords."""
    if not text or not keywords:
        return False
    search_text = text.lower() if KEYWORDS_CASE_INSENSITIVE else text
    for keyword in keywords:
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

    output_channels = _get_output_channels()
    if not output_channels:
        print("Error: Configure at least one output. Set TELEGRAM_FORWARD_TO + TELEGRAM_KEYWORDS "
              "(or TELEGRAM_FORWARD_TO_1 + TELEGRAM_KEYWORDS_1).", flush=True)
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
        for dest, keywords in output_channels:
            if not message_contains_keywords(text, keywords):
                continue
            try:
                await event.forward_to(dest)
                print(f"Forwarded to {dest} from {chat.title}: {text[:80]}...", flush=True)
            except Exception as e:
                print(f"Failed to forward to {dest}: {e}", flush=True)

    await client.start()
    for i, (dest, kw) in enumerate(output_channels, 1):
        print(f"Channel {i}: forwarding to {dest} (keywords: {kw})", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
