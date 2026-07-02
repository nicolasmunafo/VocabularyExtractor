from deep_translator import PonsTranslator
from deep_translator import GoogleTranslator
from deep_translator import LingueeTranslator
import time
import random

from typing import List
from VocabularyLLM import AIModel

class WordsTranslator:
    def __init__(self):
        pass

    def get_translations_api(self, final_list: List[str], translator: str="google") -> List[List[str]]:
        translated_list = []
        
    # https://deep-translator.readthedocs.io/en/latest/usage.html

        for word in final_list:
            '''
            Tests:
            DeepL: requires an API key           
            LingueeTranslator: Returns several synonyms but it doesn't allow scraping, so no    
            GoogleTranslator: Returns only the first, most common translation
            Pons: Returns 'NoneType' object has no attribute 'findAll'
            '''
            if translator == "google":
                translation_es = GoogleTranslator(source='german', target='spanish').translate(word)
                translation_en = GoogleTranslator(source='german', target='en').translate(word)
            elif translator == "pons":
                translation_es = PonsTranslator(source='german', target='spanish').translate(word)
                translation_en = PonsTranslator(source='german', target='en').translate(word)
            elif translator == "linguee":
                translation_es = LingueeTranslator(source='german', target='spanish').translate(word, return_all=True)
                translation_en = LingueeTranslator(source='german', target='english').translate(word, return_all=True)        
            time.sleep(random.uniform(1.5,3.0))

            translated_list.append([word, translation_es, translation_en])
       
        return translated_list    

    
    def get_translations_llm(self, final_list: List[str], ollama_model: AIModel) -> List[List[str]]:
        translated_list = []
        
        prompt_es = "Translate this German word into Spanish, with no explanations, no extra text, just the words for the translation: "
        prompt_en = "Translate this German word into English, with no explanations, no extra text, just the words for the translation: "
        
        for word in final_list:
            translation_es = ollama_model.respond_prompt(prompt_es + word)
            translation_en = ollama_model.respond_prompt(prompt_en + word)
            translated_list.append([word, translation_es, translation_en])
        
        return translated_list
    
    def get_translations_llm_complete(self, final_list: List[str], ollama_model: AIModel) -> List[List[str]]:
        translated_list: List[List[str]]
        
        prompt = f"""
                Translate the following German words into Spanish and English: {final_list}.
                For each word, generate a list containing exactly three strings in this specific order:
                ["german_word", "spanish_translation", "english_translation"]
                """

        translated_list = ollama_model.respond_prompt_list(prompt)
        
        return translated_list