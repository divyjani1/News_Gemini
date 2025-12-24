from Image_to_text import images_to_text_dict
from ..db_with_translate import translate_text

async def store_text_in_db():
    guj_text=images_to_text_dict("Photo")
    print("gujrati:",guj_text)
    english_text=await translate_text(guj_text)
    print("english:",english_text)

