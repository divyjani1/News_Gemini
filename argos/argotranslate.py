import os
from PIL import Image
import pytesseract
from argostranslate import package, translate

# -----------------------------
# Step 0: Install Gujarati→English model if not already
# -----------------------------
# Download the model once from Argos Open Tech
model_path = "gu_en.argosmodel"  # download manually or provide path
if not os.path.exists(model_path):
    import requests
    url = "https://www.argosopentech.com/argospm/index/install/gu_en.argosmodel"
    r = requests.get(url)
    with open(model_path, "wb") as f:
        f.write(r.content)
    package.install_from_path(model_path)

# Reload languages after installing
installed_languages = translate.get_installed_languages()
from_lang = None
to_lang = None
for lang in installed_languages:
    if lang.code == "gu":
        from_lang = lang
    if lang.code == "en":
        to_lang = lang

if not from_lang or not to_lang:
    raise Exception("Gujarati or English language model not installed properly.")

# -----------------------------
# Step 1: Function to translate text
# -----------------------------
def translate_text(text):
    return from_lang.get_translation(to_lang).translate(text)

# -----------------------------
# Step 2: Process images in a folder
# -----------------------------
IMAGE_DIR = "./images"  # Change this to your images folder
results = {}

for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(IMAGE_DIR, filename)
        try:
            # Extract text from image
            img = Image.open(img_path)
            text_gu = pytesseract.image_to_string(img, lang="guj")  # Gujarati OCR
            text_gu = text_gu.strip()
            
            # Translate to English
            if text_gu:
                translated_text = translate_text(text_gu)
            else:
                translated_text = ""
            
            results[filename] = translated_text
            print(f"{filename} -> {translated_text}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# -----------------------------
# Step 3: Results dictionary
# -----------------------------
print("\nAll translations:")
for k, v in results.items():
    print(f"{k}: {v}")
