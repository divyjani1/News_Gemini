import asyncio
# from googletrans import Translator
# from Db.db import db# motor async collection
from tools.Image_to_text import images_to_text_dict
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

from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

API_KEY = API_URL
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"



async def translate_text(dicto):
    translated_dict = {}  # Store translations

    for key, value in dicto.items():
        print(f"key:{key},\n value:{value}")
        payload = {
    "model": "gemini-2.5-flash",
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": f"""
You are a professional translation assistant.

Translate the following Gujarati text into English.
Return the result strictly as JSON with the key "{key}".

Text:
{value}
"""
                }
            ]
        }
    ]
}

        response = requests.post(
            url,
            params={"key":API_KEY},
            headers={
                "Content-Type": "application/json",
                # "Authorization": f"Bearer {API_KEY}"
            },
            json=payload
        )

        if response.status_code == 200:
            try:
                resp_json = response.json()
                # The text is inside resp_json['candidates'][0]['content'][0]['text']
                translated_text = resp_json['candidates'][0]['content'][0]['text']
                translated_dict[key] = translated_text
                res= await db["english"].insert_one({key:translate_text})
            except Exception as e:
                print(f"Error parsing response for key {key}: {e}")
                translated_dict[key] = None
        else:
            print(f"API Error for key {key}: Status {response.status_code}, Body: {response.text}")
            translated_dict[key] = None

    return translated_dict

async def main():
    result=await images_to_text_dict("Photo")
    res=await translate_text(result)
    print(res)

if __name__ == "__main__":
    asyncio.run(main())