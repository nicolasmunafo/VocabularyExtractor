from PIL import Image, ImageOps
from pathlib import Path
from typing import List
import numpy as np
import re
from VocabularyLLM import AIModel
# import asyncio
# from winocr import recognize_pil
import os
import pytesseract
import easyocr

import gspread


def get_text_from_img(img_path: str) -> List:
    
    # Open the file
    reader = easyocr.Reader(['de'], gpu=True)
    pil_img =Image.open(img_path).convert('RGB')

    # Transpose the file (cause it may be rotated) and crop it to reduce any noise
    pil_img = ImageOps.exif_transpose(pil_img)
    left_column = pil_img.crop((0, 0, int(pil_img.width*2/5), pil_img.height))

    # Convert the image into a numpy array for EasyOCR and return the text list
    img_array = np.array(left_column)
    return reader.readtext(img_array, detail=0)


def get_files_from_dir(path: Path) -> List[str]:
    return list(path.glob("*"))


def add_translation_list(img_text: List[str]) -> List[str]:
    # Remove any strings that are not proper words
    final_list = cleanup_list(img_text)
    # print(final_list)
    return final_list
    # 
    # print(sum([len(str_len) for str_len in final_list]))

def cleanup_list(img_text: List[str]):
    # for word in img_text:
    #     result = re.match(r"^[A-Za-zÄÖÜäöüß(),.⸚-]+$", word)
    #     print(result)
    
    match_pattern = r"^[A-Za-zÄÖÜäöüß(),;.⸚ -][A-Za-zÄÖÜäöüß(),;.⸚ -]+$"
    return [word for word in img_text if re.match(match_pattern, word)]
    # return [[word,"tr_es","tr_en"] for word in img_text if re.match(match_pattern, word)]

        


def save_contents_file(words_list: List[List[str]]):
    
    credentials_path = Path.cwd() / "VocabularyExtractor" / "carbon-vault-500208-h2-731a20096a02.json"
    SAMPLE_SPREADSHEET_ID = "1jJ7F6uaVSznuRKUCVaU5Qg5NcWwlv3K1iAl0zzxUlH4"

    gc = gspread.service_account(filename=credentials_path)
    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    # sh = gc.open("Exact Name Of Your Spreadsheet")
    sh.sheet1.append_rows(words_list)
    # print(sh.sheet1.get("A1"))
    


def main():
    
    words_list =[]

    lektion_path = Path("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/Images/Lektion 1/")

    print("test")
    img_files = get_files_from_dir(lektion_path)

    # words_list = ["Zutaten", "Postleitzahl", "Diversidad", "Zoll", "Briefumschlag"]

    ollama_model = AIModel()

    for img in img_files:
        img_text = get_text_from_img(img)
        # add_translation_list(img_text)
        words_list.append(add_translation_list(img_text))
        # break

    # words_list = [["Lernziele", "Objetivos de aprendizaje", "Educational goals"], ["Ausbildung", "Formación profesional", "Professional training"], ["Zollinhaltserklärung", "Declaración del contenido fiscal", "Fiscal content declaration"]]
    
    response = ollama_model.respond_prompt(f"""Can you translate these German words in Spanish and English? {words_list}. 
        Just with one or two short translations of each word.
        Can you also write the results as python lists, [[word1, translation spanish, translation english], [word2, translation spanish, translation english]].
                                           Do not write anything else but just the list""")

    save_contents_file(response)

    





    # ----------------------------------------------------------------
    # EasyOCR
    # ----------------------------------------------------------------
 
    # reader = easyocr.Reader(['de'], gpu=True)

    # pil_img =Image.open("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/Images/Lektion 1/IMG_4232.JPG").convert('RGB')
    # pil_img = ImageOps.exif_transpose(pil_img)
    # MAX_WIDTH = 1000
    # left_column = pil_img.crop((0, 0, int(pil_img.width), pil_img.height))
    # # pil_img.thumbnail((MAX_WIDTH, MAX_WIDTH))
    # img_array = np.array(left_column)
    
    # # img_array = np.array(pil_img)
    # result = reader.readtext(img_array, detail=0)

    # # reader = easyocr.Reader(['de'], gpu=False)

    # # 1. Load original full page
    # page = Image.open(r"C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/Images/Lektion 1/IMG_4232.JPG")
    # page = ImageOps.exif_transpose(page)

    # # 2. Manually crop roughly the same region as in Windows
    # # Adjust these numbers by trial until it visually matches
    # crop = page.crop((0, 0, int(page.width*2/5), page.height))

    # # 3. Save the crop to inspect it
    # crop.save(r"C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/Images/Lektion 1/py_crop.jpg", quality=95, subsampling=0)

    # # 4. OCR that crop
    # img_array = np.array(crop)
    # result = reader.readtext(img_array, detail=0, paragraph=True)
    # print(result)
    
    
    # ratio = MAX_WIDTH / pil_img.width
    # new_size = (MAX_WIDTH, int(pil_img.height * ratio))
    # pil_img.resize(new_size,Image.LANCZOS)
    
    
    # pil_img =Image.open("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/IMG_8173_LWS_5.jpg").convert('RGB')
    # Crop using two coordinates, (left, upper, right, lower) means two points, (left, upper) and (right, lower)
    # https://stackoverflow.com/questions/9983263/how-to-crop-an-image-using-pil




    # result = reader.readtext("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/IMG_8173_LWS.jpg", detail=0)
    # result = reader.readtext("C:/Users/Nicolas/Desktop/Trámites BCN/Documentación/Nicolas Alejandro Munafo Lorenzo - EU Passport.jpg", detail=0)
    # print(result)

    # ----------------------------------------------------------------
    # WinOCR
    # ----------------------------------------------------------------

# async def main():

#     # img = Image.open("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/IMG_8173.jpg")#.convert("RGB")
#     img = Image.open("C:/Users/Nicolas/Desktop/Trámites BCN/Documentación/Nicolas Alejandro Munafo Lorenzo - EU Passport.jpg")#.convert("RGB")
#     result = await recognize_pil(img, lang="de")
#     print(result.text)

    # ----------------------------------------------------------------
    # Tesseract
    # ----------------------------------------------------------------   
    
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # # image_path = Path("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/IMG_8173.jpg")
    # image_path = Path("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/Images/Lektion 1/IMG_4232.JPG")
    # # image_path = Path("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/IMG_8173_LWS_5.jpg")
    # img = Image.open(str(image_path)).convert("RGB")
    # img = ImageOps.exif_transpose(img)
    # MAX_WIDTH = 1000
    # left_column = img.crop((0, 0, int(img.width/2), img.height))
    # img.thumbnail((1800, 1800))
    # print(img.mode, img.size, img.format)

    # text = pytesseract.image_to_string(img, lang="deu")
    # print(text)

# if __name__ == "__main__":
#     asyncio.run(main())
    
if __name__ == "__main__":
    main()