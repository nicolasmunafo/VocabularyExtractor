from pathlib import Path
from typing import List

import re
from VocabularyLLM import AIModel
from config.config_reader import ConfigReader
from classes.words_translator import WordsTranslator
from classes.image_reader import ImageReader
from classes.gsheet_manager import GSheetManager


def get_files_from_dir(path: Path) -> List[str]:
    return list(path.glob("*"))


def add_translation_list(img_text: List[str], ollama_model: AIModel) -> List[List[str]]:
    # Remove any strings that are not proper words
    final_list = cleanup_list(img_text)
    translator = WordsTranslator()
    # translation_list = translator.get_translations_api(final_list, "google")
    translation_list = translator.get_translations_llm_complete(final_list, ollama_model)
    return translation_list


def cleanup_list(img_text: List[str]):
    # for word in img_text:
    #     result = re.match(r"^[A-Za-zÄÖÜäöüß(),.⸚-]+$", word)
    #     print(result)
    match_pattern = r"^[A-Za-zÄÖÜäöüß(),;.⸚ -][A-Za-zÄÖÜäöüß(),;.⸚ -]+$"
    return [word for word in img_text if re.match(match_pattern, word)]
    # return [[word,"tr_es","tr_en"] for word in img_text if re.match(match_pattern, word)]
    


def main():
    
    level = "A1"

    lektion = "Lektion 2"

    words_list = []

    config_reader = ConfigReader()

    image_reader = ImageReader()

    gsheet_manager = GSheetManager()

    # credentials_path = Path.cwd() / config_reader.gsheets_credential
    # sheet_id = config_reader.sheet_id[level]

    # gc = gspread.service_account(filename=credentials_path)
    # sh = gc.open_by_key(sheet_id)

    # gsheet_manager.check_existing_sheet(lektion, sh)

    lektion_path = Path(config_reader.images_path) / level / lektion

    img_files = get_files_from_dir(lektion_path)

    ollama_model = AIModel(config_reader.ollama_url)

    for img in img_files:
        img_text = image_reader.get_text_from_img(img)
        words_list.extend(add_translation_list(img_text, ollama_model))         # With append it adds the list as a sublist, but here we need to extend it
        break
  
    gsheet_manager.save_contents_file(words_list, config_reader, level, lektion)


    
    
if __name__ == "__main__":
    main()