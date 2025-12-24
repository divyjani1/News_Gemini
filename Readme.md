App is divided in 3 parts
1)First part is getting image data from the given link.
bot.py- using playwright,we had given link of website,so it will extract the images from that website and store those in folder named sandesh -where you will find images of each an every article,currently no logic given for duplicate images.
For running this you explicity need to run python3 bot.py if in linux.
2)Extracting text from Translating text from the extracted text in english and storing it into mongo db collection
analyze_all.py-It will analyze single function for the whole and generate that data into text.
You need to explicitly run python3 analyze_all.py 
--------------OR-----------------------
2)
    1)use opensource library pytesseract from extracting text from images 
    it will store gujrati text in db ,for that run python3 Image_to_text.py,we can use it inside translate_text function in db_with_translate.py
    2)then use translate_text function in db_with_translate.py for translating gujarati text into english using gemini_api ,run python3 db_with_translate.py

3)Get the data from db using get_data function and then take the user prompt and compare the words and get the matched articles store those articles in object and serve it to the prompt and you will get the result according to the prompt 

the sandesh image folder-where all images stored 
photo-manually created folder 
