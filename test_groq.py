
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key,
    timeout=120,
    max_retries=2
)

languages = {
    "English": "Summarize this text in one sentence in English: Artificial intelligence is transforming education through personalized learning and automated grading.",
    "French": "Résume ce texte en une phrase en français : L'intelligence artificielle transforme l'éducation grâce à l'apprentissage personnalisé et à la correction automatique.",
    "Arabic": "لخص هذا النص في جملة واحدة باللغة العربية: يساهم الذكاء الاصطناعي في تطوير التعليم من خلال التعلم الشخصي والتصحيح الآلي."
}

for language, prompt in languages.items():
    print(f"\n--- {language} ---")

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            reasoning_effort="none",
            temperature=0.7,
            max_completion_tokens=300
        )

        result = response.choices[0].message.content

        if result:
            print(result.strip())
        else:
            print("EMPTY RESPONSE")

    except Exception as error:
        print(type(error).__name__, str(error))
