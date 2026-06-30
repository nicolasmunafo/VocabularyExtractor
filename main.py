from PIL import Image, ImageOps
from pathlib import Path
from typing import List
import numpy as np
import re
from VocabularyLLM import AIModel
from Config.config_reader import ConfigReader

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

        

def save_contents_file(words_list: List[List[str]], config_reader: ConfigReader):
    
    credentials_path = Path.cwd() / config_reader.gsheets_credential
    SAMPLE_SPREADSHEET_ID = config_reader.sheet_id   
    # credentials_path = Path.cwd() / "VocabularyExtractor" / "carbon-vault-500208-h2-731a20096a02.json"
    # SAMPLE_SPREADSHEET_ID = "1jJ7F6uaVSznuRKUCVaU5Qg5NcWwlv3K1iAl0zzxUlH4"

    gc = gspread.service_account(filename=credentials_path)
    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    sh.sheet1.append_rows(words_list)
    # print(sh.sheet1.get("A1"))
    


def main():
    
    words_list = []

    config_reader = ConfigReader()

    lektion_path = Path(config_reader.images_path) / "Lektion 1" 

    img_files = get_files_from_dir(lektion_path)

    # words_list = ["Zutaten", "Postleitzahl", "Diversidad", "Zoll", "Briefumschlag"]

    ollama_model = AIModel(config_reader.ollama_url)

    for img in img_files:
        img_text = get_text_from_img(img)
        # add_translation_list(img_text)
        words_list.append(add_translation_list(img_text))
        break

    # words_list = [["Lernziele", "Objetivos de aprendizaje", "Educational goals"], ["Ausbildung", "Formación profesional", "Professional training"], ["Zollinhaltserklärung", "Declaración del contenido fiscal", "Fiscal content declaration"]]
    
    prompt = f"""
            You are a translation engine. 
            Translate each German word into Spanish and English.

            Return ONLY a list of lists in this exact format:
            [
            ["word", "spanish", "english"],
            ...
            ]

            Rules:
            - No explanations.
            - No extra text.
            - No extra fields.
            - No synonyms beyond one translation per language.
            - Do NOT add punctuation outside the JSON.
            - If you were not able to find a translation, just leave it blank, but always create a list of lists with three elements each, no more, no less

            Words: {words_list}
            """

    response = ollama_model.respond_prompt(prompt)

    # save_contents_file(words_list, config_reader)
    save_contents_file(response, config_reader)

    
    
if __name__ == "__main__":
    main()


'''
TODO:
- Refactor
- Test with direct translations
- Modify the response 

'''