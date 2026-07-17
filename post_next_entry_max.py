#!/usr/bin/env python3
import asyncio
import csv
import json
import os
import re
from datetime import datetime

try:
      from maxapi import MAX
except ImportError:
      print("Error: maxapi library not installed. Run: pip install maxapi")
      exit(1)


class TolstoyMaxBot:
      def __init__(self, token: str, chat_id: str):
                self.max_api = MAX(token=token)
                self.chat_id = chat_id
                self.csv_file = "tolstoy_diary_autopost_modern.csv"
                self.state_file = "state_max.json"
                self.char_limit = 3900

      def load_state(self) -> dict:
                """Load posting state from file."""
                if os.path.exists(self.state_file):
                              with open(self.state_file, "r", encoding="utf-8") as f:
                                                return json.load(f)
                                        return {"last_index": -1}

            def save_state(self, state: dict) -> None:
                      """Save posting state to file."""
                      with open(self.state_file, "w", encoding="utf-8") as f:
                                    json.dump(state, f, ensure_ascii=False, indent=2)

                  def load_entries(self) -> list:
                            """Load diary entries from CSV file."""
                            entries = []
                            try:
                                          with open(self.csv_file, "r", encoding="utf-8") as f:
                                                            reader = csv.DictReader(f)
                                                            for row in reader:
                                                                                  entries.append(row)
                            except FileNotFoundError:
                                          print(f"Error: {self.csv_file} not found")
                                          exit(1)
                                      return entries

    def split_message(self, text: str) -> list:
              """Split message into chunks respecting char limit and paragraph breaks."""
        chunks = []
        paragraphs = text.split("\n\n")
        current_chunk = ""

        for para in paragraphs:
                      if len(current_chunk) + len(para) + 2 <= self.char_limit:
                                        if current_chunk:
                                                              current_chunk += "\n\n"
                                                          current_chunk += para
else:
                if current_chunk:
                                      chunks.append(current_chunk)
                if len(para) > self.char_limit:
                                      sentences = re.split(r'([.!?]\s+)', para)
                    temp_chunk = ""
                    for i in range(0, len(sentences), 2):
                                              sent = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
                                              if len(temp_chunk) + len(sent) <= self.char_limit:
                                                                            temp_chunk += sent
else:
                            if temp_chunk:
                                                              chunks.append(temp_chunk)
                                                          temp_chunk = sent
                    if temp_chunk:
                                              chunks.append(temp_chunk)
else:
                    current_chunk = para

        if current_chunk:
                      chunks.append(current_chunk)

        return chunks

    async def send_message(self, text: str) -> None:
              """Send message to MAX chat."""
        await self.max_api.sendMessage(
                      chat_id=int(self.chat_id),
                      text=text
        )

    async def post_next_entry(self) -> None:
              """Post the next diary entry to MAX."""
        state = self.load_state()
        entries = self.load_entries()

        next_index = state["last_index"] + 1
        if next_index >= len(entries):
                      print("All entries have been posted")
            return

        entry = entries[next_index]
        date_str = entry.get("date", "Unknown date")
        text = entry.get("text", "")

        message = f"📖 {date_str}\n\n{text}"
        chunks = self.split_message(message)

        for i, chunk in enumerate(chunks):
                      try:
                                        await self.send_message(chunk)
                print(f"Posted chunk {i + 1}/{len(chunks)}")
except Exception as e:
                print(f"Error posting chunk {i + 1}: {e}")
                return

        state["last_index"] = next_index
        self.save_state(state)
        print(f"Successfully posted: {date_str}")


async def main():
      token = os.getenv("MAX_BOT_TOKEN")
    chat_id = os.getenv("MAX_CHAT_ID")

    if not token or not chat_id:
              print("Error: MAX_BOT_TOKEN and MAX_CHAT_ID environment variables must be set")
        exit(1)

    bot = TolstoyMaxBot(token, chat_id)
    await bot.post_next_entry()


if __name__ == "__main__":
      asyncio.run(main())
