import base64

from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

def load_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

GEMINI_API_KEY = API_URL

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
    "/gemini-2.5-flash:generateContent"

)