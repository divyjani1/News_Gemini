import asyncio
# from googletrans import Translator
# from Db.db import db# motor async collection
from Image_to_text import images_to_text_dict
# translator = Translator()

# from argostranslate import package, translate

# package.update_package_index()

# # Get available packages
# available_packages = package.get_available_packages()

# # Find Gujarati → English package
# gu_en_pkg = next(
#     p for p in available_packages
#     if p.from_code == "gu" and p.to_code == "en"
# )

# # Install it
# package.install_from_path(gu_en_pkg.download())

# installed_languages = translate.get_installed_languages()
# gu = next(l for l in installed_languages if l.code == "gu")
# en = next(l for l in installed_languages if l.code == "en")

# async def translate_text(dicto):
#     print("Translate text run")
#     if not dicto:
#         print("Invalid data")
#         return {"message":"Invalid Data"}
#     print(dicto.items())
#     result=[]
#     translator = gu.get_translation(en)
#     for key,value in dicto.items():
       

#        english_text = translator.translate(value)
#         # english_text =translated.text
#        print("GUJARATI:", value[:200])
#        print("ENGLISH :", english_text[:200])
#         # print("IIIIIIIIIIIIIIIIIIIIIIIIIII",english_text)
#         # result.append({key:english_text})
        
    

#        resp=await db["english_text"].insert_one({key:english_text})
#        print("Stored:", str(resp))
    
#     # return result

# async def main():
#     result=await images_to_text_dict("Photo")
#     res=await translate_text(result)
#     print(res)

# if __name__ == "__main__":
#     asyncio.run(main())


import requests
import os
from Db.db import db
import json
from dotenv import load_dotenv
import os
import re

load_dotenv()

API_URL = os.getenv("API_URL")

API_KEY = API_URL
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"



async def translate_text():
    results = []

    docs = await db["gujrati_text"].find().to_list(None)
    i=0
    for doc in docs:
        if i==5:
            break
        i+=1
        gu_text = doc.get("text")
        image_name = doc.get("image_name")

        if not gu_text:
            continue

        payload = {
            "model": "gemini-2.5-flash",
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text":  f"""
You are a professional news translation and structured information extraction assistant
specialized in OCR-extracted Gujarati newspaper content.

Your task MUST follow ALL rules below. These rules are STRICT and NON-NEGOTIABLE.

====================================================
CORE OBJECTIVE
====================================================

Given Gujarati news text that may contain OCR noise, strap lines, and merged layout content,
you MUST:

1. Accurately translate the content into English.
2. Correctly identify the TRUE newspaper headline.
3. Extract the complete translated article text WITHOUT summarization.
4. Extract exactly ONE category and ONE location (city or place).

====================================================
MANDATORY PROCESS (INTERNAL – DO NOT SKIP)
====================================================

Before extracting fields, you MUST internally perform the following steps:

STEP 1: TEXT NORMALIZATION
- Ignore OCR noise, repeated symbols, layout artifacts, and ads.
- Preserve the original meaning, facts, and structure.

STEP 2: HEADLINE IDENTIFICATION (CRITICAL)
- Every news article ALWAYS has a headline.
- The headline may appear on the first line OR the second line OR later.
- The first line MAY be a strap line or explainer and MUST NOT be selected as the headline unless it clearly represents the main news event.

You MUST identify the headline using these rules:
- The headline is the most concise line that describes the CORE NEWS EVENT.
- It is factual, event-driven, and not descriptive or emotional.
- It typically mentions an incident, action, or outcome (e.g., attack, death, decision, result).
- Strap lines, background descriptions, or emotional context are NOT headlines.

Selecting the wrong headline is considered a FAILURE.

STEP 3: FULL TEXT EXTRACTION
- The "full_text" MUST be the COMPLETE English translation of the entire article content.
- Do NOT summarize, shorten, paraphrase, or omit any information.
- Preserve all names, numbers, dates, places, and facts exactly as stated.

STEP 4: LOCATION EXTRACTION (IMPORTANT)
- If a city name is explicitly mentioned, use it.
- If no city is mentioned, but another location (area, country, region, landmark) is mentioned,
  you MUST return that location instead.
- Location MUST be explicitly present in the text.
- If no location of any kind is mentioned, return null.

STEP 5: CATEGORY SELECTION
- Select exactly ONE most appropriate category based ONLY on the article’s main event.
- Do NOT infer or guess.

====================================================
OUTPUT FIELD RULES (STRICT)
====================================================

You MUST return ONLY the following fields:

- headline: The correctly identified headline (translated to English).
- full_text: The complete English translation of the article.
- categories: EXACTLY ONE category string OR null.
- city: EXACTLY ONE city or location string OR null.

====================================================
ALLOWED CATEGORY VALUES (STRICT)
====================================================

Politics, Crime, Sports, Business, Health, Education, Entertainment,
Technology, Weather, Local News, International News

====================================================
CARDINALITY RULES (NON-NEGOTIABLE)
====================================================

- "categories" MUST be a SINGLE string, NOT an array.
- "city" MUST be a SINGLE string, NOT an array.
- If multiple candidates exist, select ONLY the MOST RELEVANT ONE.
- If a value cannot be confidently determined from the text, return null.

====================================================
OUTPUT FORMAT RULES (CRITICAL)
====================================================

- Output MUST be valid JSON.
- Output MUST contain ONLY the JSON object.
- Do NOT include explanations, comments, or markdown.
- Do NOT add extra keys.
- Use null (not empty string, not empty array) when a value cannot be determined.

====================================================
GUJARATI NEWS TEXT
====================================================

{gu_text}

"""

                        }
                    ]
                }
            ]
        }

        response = requests.post(
            url,
            params={"key": API_KEY},
            headers={"Content-Type": "application/json"},
            json=payload
        )

        if response.status_code != 200:
            print("API error:", response.text)
            continue

        try:
            gemini_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            print(gemini_text)
            parsed_json = extract_json(gemini_text)

            # parsed_json["source_image"] = image_name

            results.append(parsed_json)

            # Optional DB insert
            await db["english_text_by_translations2"].insert_one(parsed_json)

        except Exception as e:
            print("Parsing error:", e)

    return results

def extract_json(text: str) -> dict:
    """
    Extracts and parses the first valid JSON object from model output.
    """
    try:
        # Remove markdown fences
        text = re.sub(r"```(?:json)?", "", text).strip()

        # Extract JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found")

        json_str = match.group(0)

        return json.loads(json_str)

    except Exception as e:
        raise ValueError(f"Invalid JSON from model: {e}")

async def main():
    # result=await images_to_text_dict("Photo")
    res=await translate_text()
    print(res)

if __name__ == "__main__":
    asyncio.run(main())