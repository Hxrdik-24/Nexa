import datetime
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Gemini client
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Retry configuration
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 8      # seconds


def apiprocess(command):
    # Command length check
    if len(command) > 50:
        return "Error: Command too long! Please keep it under 25 characters."

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Sahi model aur method call
            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash",
                contents=f"Answer strictly in 1-2 short sentences: {command}",
            )

            reply_text = response.text.strip()

            # Log successful request
            log_entry = (
                f"[{current_time}] SUCCESS | Command: '{command}'\n"
                f"   - Attempt: {attempt}\n"
                f"   - Response: {reply_text}\n"
                "--------------------------------------------------\n"
            )

            with open("data/logs.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)

            return reply_text

        except Exception as e:
            # Last attempt failed
            if attempt == MAX_RETRIES:
                error_log = (
                    f"[{current_time}] API FAILED\n"
                    f"   - Command: '{command}'\n"
                    f"   - Attempts: {MAX_RETRIES}\n"
                    f"   - Error: {str(e)}\n"
                    "--------------------------------------------------\n"
                )

                with open("data/logs.txt", "a", encoding="utf-8") as f:
                    f.write(error_log)

                return "Error: Gemini API request failed after multiple retries."

            # Exponential backoff
            retry_delay = min(
                INITIAL_RETRY_DELAY * (2 ** (attempt - 1)),
                MAX_RETRY_DELAY,
            )

            retry_log = (
                f"[{current_time}] RETRY\n"
                f"   - Attempt: {attempt}/{MAX_RETRIES}\n"
                f"   - Retrying in: {retry_delay}s\n"
                f"   - Error: {str(e)}\n"
            )

            with open("data/logs.txt", "a", encoding="utf-8") as f:
                f.write(retry_log)

            time.sleep(retry_delay)

    return "Error: Unable to process request."