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
    # print('textyyyyyy:',compiled_text)
    payload = {
        "contents": [
            # {
            #     "role": "system",
            #     "parts": [{
            #         "text": (
            #             "You are a factual news assistant.\n"
            #             "Answer ONLY from provided articles.\n"
            #             "If not found, say 'Not present in today's newspaper'."
            #         )
            #     }]
            # },
            {
                "role": "user",
                "parts": [{
                    "text": (          
                       "You are a factual news assistant.\n"
                    "Answer ONLY from the provided articles.\n"
                    "Do NOT generate information that is not present.\n"
                    "Follow these rules strictly:\n"
                    "1. Match the query with the fields: 'headline', 'full_text', 'category', 'city'.\n"
                    "2. Filter by city or category if mentioned.\n"
                    "3. Return ONLY the fields requested in the query.\n"
                    "   - For example, if asked 'only headlines', return only a JSON array of headlines.\n"
                    "   - If asked 'category and city', return only those fields.\n"
                    "4. Return results as a valid JSON array. Do NOT add any extra text, commentary, or explanations.\n"
                    "5. If no articles match, respond exactly: \"Not present in today's newspaper.\"\n\n"
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
    # print(response.status_code)
    # print(response.text)
    response.raise_for_status()

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]
