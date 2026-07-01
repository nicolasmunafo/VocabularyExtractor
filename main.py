from pathlib import Path
from typing import List

import re
from VocabularyLLM import AIModel
from config.config_reader import ConfigReader
from classes.words_translator import WordsTranslator
from classes.image_reader import ImageReader

import gspread


def get_files_from_dir(path: Path) -> List[str]:
    return list(path.glob("*"))


def add_translation_list(img_text: List[str], ollama_model: AIModel) -> List[List[str]]:
    # Remove any strings that are not proper words
    final_list = cleanup_list(img_text)
    translator = WordsTranslator()
    translation_list = translator.get_translations_api(final_list, "google")
    return translation_list


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

    gc = gspread.service_account(filename=credentials_path)
    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    sh.sheet1.append_rows(words_list)
    # print(sh.sheet1.get("A1"))
    


def main():
    
    words_list = []

    config_reader = ConfigReader()

    image_reader = ImageReader()

    lektion_path = Path(config_reader.images_path) / "Lektion 1" 

    img_files = get_files_from_dir(lektion_path)

    # words_list = ["Zutaten", "Postleitzahl", "Diversidad", "Zoll", "Briefumschlag"]

    ollama_model = AIModel(config_reader.ollama_url)

    for img in img_files:
        img_text = image_reader.get_text_from_img(img)
        # add_translation_list(img_text)
        words_list.append(add_translation_list(img_text, ollama_model))
        break

    # words_list = [["Lernziele", "Objetivos de aprendizaje", "Educational goals"], ["Ausbildung", "Formación profesional", "Professional training"], ["Zollinhaltserklärung", "Declaración del contenido fiscal", "Fiscal content declaration"]]
    
    # save_contents_file(words_list, config_reader)
    # save_contents_file(response, config_reader)

    
    
if __name__ == "__main__":
    main()


'''
TODO:
- Refactor
- Test with direct translations
- Modify the response 

'''