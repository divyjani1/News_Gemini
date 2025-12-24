# import os
# from PIL import Image
# import pytesseract
# from .Db.db import db

# async def images_to_text_dict(image_dir, lang="guj"):
#     """
#     Convert all images in a directory to text using Tesseract OCR.

#     Args:
#         image_dir (str): Path to directory containing images
#         lang (str): OCR language (default: 'guj')

#     Returns:
#         dict: { "image_name.jpg": "extracted text", ... }
#     """

#     ocr_data = {}

#     for filename in sorted(os.listdir(image_dir)):
#         if filename.lower().endswith((".jpg", ".jpeg", ".png")):
#             image_path = os.path.join(image_dir, filename)

#             try:
#                 image = Image.open(image_path)
#                 text = pytesseract.image_to_string(image, lang=lang)
#                 ocr_data[filename] = text.strip()
#                 resp=await db["gujrati_text"].insert_one({filename:ocr_data[filename]})
#                 print("Stored:", str(resp))
#             except Exception as e:
#                 ocr_data[filename] = f"OCR_FAILED: {e}"
                
#     return ocr_data

import os
import asyncio
from PIL import Image
import pytesseract
from Db.db import db   # absolute import ONLY

import re



##Conversion into guj_text into clean text
##
def clean_gujarati_ocr_text(text: str) -> str:
    """
    Cleans OCR noise from Gujarati newspaper text
    without converting it into headline/body.
    """

    if not text:
        return ""

    # Remove OCR garbage symbols
    text = re.sub(r"[₹$€^*_+=<>|~]", "", text)

    # Remove repeated separator characters
    text = re.sub(r"[-_=]{2,}", " ", text)

    # Remove isolated page numbers or stray digits on lines
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    # Fix broken words caused by OCR line wraps
    text = re.sub(r"(\S)-\n(\S)", r"\1\2", text)

    # Normalize spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Normalize newlines (keep paragraphs)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing spaces per line
    text = "\n".join(line.strip() for line in text.splitlines())

    return text.strip()

#Clean Text function Ends

def ocr_sync(image, lang):
    return pytesseract.image_to_string(image, lang=lang)

async def images_to_text_dict(image_dir, lang="guj"):
    ocr_data = {}

    loop = asyncio.get_running_loop()

    for filename in sorted(os.listdir(image_dir)):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(image_dir, filename)

        try:
            with Image.open(image_path) as image:
                text = await loop.run_in_executor(
                    None, ocr_sync, image, lang
                )

            cleaned_text = text.strip()

            cleaned_text=clean_gujarati_ocr_text(cleaned_text)
            ocr_data[filename] = cleaned_text

            existing = await db["gujrati_text"].find_one({
            "filename": filename,
            "language": lang
        })

            if existing:
                print(f"Skipped {filename} (already exists)")
                ocr_data[filename] = existing.get("text")
                continue


            resp = await db["gujrati_text"].insert_one({
                "filename": filename,
                "text": cleaned_text,
                "language": lang
            })

            print(f"Stored {filename} → {resp.inserted_id}")

        except Exception as e:
            print(f"OCR failed for {filename}: {e}")
            ocr_data[filename] = None
    # print(ocr_data)
    return ocr_data

async def main():
    IMAGE_DIR = "Photo"
    result = await images_to_text_dict(IMAGE_DIR)
    print("DONE. Total images:", len(result))

if __name__ == "__main__":
    asyncio.run(main())

