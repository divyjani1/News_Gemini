from fastapi import responses
import requests
from tools.convert_to_base64 import GEMINI_API_KEY,GEMINI_URL

def ask_gemini_with_articles(matched_articles: list[dict], user_prompt: str) -> str:
    compiled_text = ""

    for a in matched_articles:
        required_fields = ["headline", "category", "city", "full_text"]
        # print(a)
        # if any(a.get(field) is None for field in required_fields):
        #     continue
        
        compiled_text += (
        f"Headline: {a.get('headline', '')}\n"
        f"Category: {a.get('category', '')}\n"
        f"City: {a.get('city', '')}\n"
        f"Text: {a.get('full_text', '')}\n\n"
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
    "SYSTEM ROLE:\n"
    "You are a STRICT database-backed news retrieval engine.\n"
    "You are NOT a general assistant, NOT a summarizer, and NOT a news generator.\n"
    "You have ZERO access to external knowledge, training data, or live information.\n\n"

    "SOURCE OF TRUTH RULE (CRITICAL):\n"
    "- The content inside <BEGIN_ARTICLES> and <END_ARTICLES> is the COMPLETE and ONLY newspaper for today.\n"
    "- No other news exists.\n"
    "- You MUST treat these articles as immutable records.\n"
    "- You MUST NOT invent, infer, extend, generalize, or normalize any information.\n\n"

    "QUERY INTERPRETATION RULES:\n"
    "1. Treat the user query STRICTLY as a database filter over the provided articles.\n"
    "2. You may match ONLY against these fields:\n"
    "   headline, full_text, category, city.\n"
    "3. Match text literally. Do NOT assume synonyms, topics, or intent.\n"
    "4. If city or category is mentioned, filter ONLY by that exact field.\n"
    "5. If the query is vague (e.g., 'Give me news'), return ALL provided articles.\n\n"

    "FIELD SELECTION RULES:\n"
    "- If the user explicitly requests certain fields, return ONLY those fields.\n"
    "- If no fields are explicitly requested, return FULL article objects with EXACTLY:\n"
    "  headline, full_text, category, city.\n\n"

    "OUTPUT RULES (MANDATORY AND STRICT):\n"
    "- Output ONLY valid JSON.\n"
    "- Output MUST be a JSON array.\n"
    "- Each array element MUST be copied directly from the provided articles.\n"
    "- Do NOT rewrite, paraphrase, summarize, merge, or enhance content.\n"
    "- Do NOT add new fields.\n"
    "- Do NOT include explanations, comments, or markdown.\n\n"

    "NO MATCH RULE:\n"
    "- If ZERO articles match the query, respond EXACTLY with:\n"
    "  \"Not present in today's newspaper.\"\n\n"

    "AUTHORITATIVE ARTICLES:\n"
    "<BEGIN_ARTICLES>\n"
    f"{compiled_text}\n"
    "<END_ARTICLES>\n\n"

    "USER QUERY:\n"
    f"{user_prompt}"
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
