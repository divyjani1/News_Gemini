from fastapi import responses
import requests
from tools.convert_to_base64 import GEMINI_API_KEY,GEMINI_URL

def ask_gemini_with_articles(matched_articles: list[dict], user_prompt: str) -> str:
    compiled_text = ""

    for a in matched_articles:
        compiled_text += (
            f"Headline: {a['headline']}\n"
            f"Category: {a['category']}\n"
            f"City: {a['city']}\n"
            f"Text: {a['full_text']}\n\n"
        )

    payload = {
        "contents": [
            {
                "role": "system",
                "parts": [{
                    "text": (
                        "You are a factual news assistant.\n"
                        "Answer ONLY from provided articles.\n"
                        "If not found, say 'Not present in today's newspaper'."
                    )
                }]
            },
            {
                "role": "user",
                "parts": [{
                    "text": (
                        f"Articles:\n{compiled_text}\n"
                        f"Question: {user_prompt}"
                    )
                }]
            }
        ]
    }

    response = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_API_KEY},
        json=payload,
        timeout=60
    )
    print(response.status_code)
    print(response.text)
    response.raise_for_status()

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]
