#!/usr/bin/env python3
import asyncio
import os
import sys

try:
      from maxapi import MAX
except ImportError:
      print("Error: maxapi library not installed")
      exit(1)


async def get_chat_id(channel_link: str):
      """Resolve channel link to numeric chat_id."""
      token = os.getenv("MAX_BOT_TOKEN")
      if not token:
                print("Error: MAX_BOT_TOKEN env var not set")
                exit(1)

      max_api = MAX(token=token)

    channel_link = channel_link.strip("/")
    if channel_link.startswith("https://"):
              channel_link = channel_link.split("/")[-1]
          if channel_link.startswith("@"):
                    channel_link = channel_link[1:]

    try:
              chat_info = await max_api.getChat(channel_link)
              chat_id = chat_info.get("id") or chat_info.get("chat_id")
              if chat_id:
                            print(f"chat_id: {chat_id}")
    else:
            print("Error: Could not extract chat_id from response")
                  print(f"Response: {chat_info}")
except Exception as e:
        print(f"Error: {e}")
        exit(1)


async def main():
      if len(sys.argv) < 2:
                print("Usage: get_chat_id.py <channel_link>")
                exit(1)

    channel_link = sys.argv[1]
    await get_chat_id(channel_link)


if __name__ == "__main__":
      asyncio.run(main())
