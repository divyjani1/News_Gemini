from Image_analysis.analyze_single import analyze_image_with_gemini
import os
import time
import asyncio
from Db.db import db


async def init_db():
    await db["english_text"].create_index(
        [("image_hash", 1)],
        unique=True
    )


async def analyze_all_images(image_dir: str) -> list[dict]:
    """
    Input:  directory of article images
    Output: list of Article dictionaries
    """

    articles = []

    for index, filename in enumerate(sorted(os.listdir(image_dir))):
        if not filename.endswith(".jpg"):
            continue

        image_path = os.path.join(image_dir, filename)
        
       


        article =await analyze_image_with_gemini(image_path)
        print("indexxxxxx:",index,"/n filename",filename)
        # article["id"] = index + 1
        article["source_image"] = filename
        
        articles.append(article)

        time.sleep(1)
        
    # print(articles)
    return articles

async def main():
    await init_db()
    res=await analyze_all_images("Photo")
    print(res)

if __name__=="__main__":
    asyncio.run(main())



