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
    return final_list


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

    
    
if __name__ == "__main__":
    main()