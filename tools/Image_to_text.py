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
            ocr_data[filename] = cleaned_text

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

# async def main():
#     IMAGE_DIR = "Photo"
#     result = await images_to_text_dict(IMAGE_DIR)
#     print("DONE. Total images:", len(result))

# if __name__ == "__main__":
#     asyncio.run(main())
