
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# ==================================================
# 1. Environment configuration
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

# ==================================================
# 2. Groq client configuration
# ==================================================

MODEL_NAME = "qwen/qwen3.8-27b"

client = Groq(
    api_key=API_KEY,
    timeout=180.0,
    max_retries=5
)

# ==================================================
# 3. Word counter
# ==================================================

def count_words(text):
    """Count words in English, French and Arabic."""
    return len(
        re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    )


# ==================================================
# 4. Summary length configuration
# ==================================================

def get_length_instruction(length, original_words):

    if length == "Short":
        target = max(8, int(original_words * 0.40))

        return (
            f"Write a concise summary of approximately "
            f"{target} words or fewer."
        )

    elif length == "Medium":
        target = max(15, int(original_words * 0.65))

        return (
            f"Write a medium-length summary of approximately "
            f"{target} words."
        )

    elif length == "Detailed":
        target = max(20, int(original_words * 0.90))

        return (
            f"Write a detailed summary of approximately "
            f"{target} words. Preserve all important information."
        )

    raise ValueError("Invalid summary length.")


# ==================================================
# 5. Main summarization function
# ==================================================

def summarize_text(
    text,
    length="Medium",
    language="Same as original"
):

    # Validate input
    if not text or not text.strip():
        raise ValueError("Please enter some text to summarize.")

    if length not in ["Short", "Medium", "Detailed"]:
        raise ValueError("Invalid summary length.")

    supported_languages = [
        "Same as original",
        "English",
        "Arabic",
        "French"
    ]

    if language not in supported_languages:
        raise ValueError("Unsupported output language.")

    original_words = count_words(text)

    length_instruction = get_length_instruction(
        length,
        original_words
    )

    # Build prompt
    prompt = f"""
You are a professional multilingual AI text summarizer.

YOUR TASK:
Summarize the provided text accurately and naturally.

OUTPUT LANGUAGE:
{language}

Language instructions:
- Same as original: detect the source language and use it.
- English: produce natural, professional English.
- Arabic: produce clear, grammatically correct Arabic.
- French: produce natural, grammatically correct French.

SUMMARY LENGTH:
{length_instruction}

IMPORTANT RULES:
1. Preserve the original meaning.
2. Include the most important information.
3. Never invent facts or add external information.
4. Preserve important names, dates and numbers.
5. Avoid unnecessary repetition.
6. Make the summary shorter than the original whenever possible.
7. Do not write an introduction or conclusion.
8. Return only the final summary.

TEXT TO SUMMARIZE:
{text}
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert multilingual AI summarizer. "
                        "Your priority is accuracy, clarity and conciseness."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            reasoning_effort="none",
            max_completion_tokens=2048
        )

        result = response.choices[0].message.content

        if not result or not result.strip():
            raise RuntimeError(
                "The AI model returned an empty response. Please try again."
            )

        return result.strip()

    except Exception as error:

        raise RuntimeError(
            f"Summarization failed: {type(error).__name__}: {error}"
        ) from error
