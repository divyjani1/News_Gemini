
from tools.match_articles import match_articles
from tools.generate_answer import ask_gemini_with_articles
from Image_to_text import images_to_text_dict
# from to_english import result
# from Image_analysis.analyze_all import analyze_all_images
from db_with_translate import translate_text
import asyncio
from Db.db import db
from get_data_from_db import get_data


async def main():
    print("Analyzing newspaper images...")
    try:
        result=await get_data()
        # ARTICLES_DB=analyze_all_images("Photo")
        # print("::::::::::::::::",ARTICLES_DB)
        # guj_text=await images_to_text_dict("Photo")
        # english_text=await translate_text(guj_text)
    
        # print("res--------------------------------------------",res)


    except Exception as e:
        print("Failed during image analysis:",e)
        result= []

    print(f"{len(result)} articles indexed.")

    while True:
        user_prompt = input("\nAsk a news question (or exit): ")

        if user_prompt.lower() == "exit":
            break

        matched = match_articles(user_prompt, result)
        # print("match:",matched)
        if not matched:
            print("No matching news found.")
            continue

        answer = ask_gemini_with_articles(matched, user_prompt)
        print("\nANSWER:\n", answer)

if __name__ == "__main__":
    asyncio.run(main())