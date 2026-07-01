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
    

    # prompt = f"""
    #         You are a translation engine. 
    #         Translate each German word into Spanish and English.

    #         Return ONLY a list of lists in this exact format:
    #         [
    #         ["word", "spanish", "english"],
    #         ...
    #         ]

    #         Rules:
    #         - No explanations.
    #         - No extra text.
    #         - No extra fields.
    #         - No synonyms beyond one translation per language.
    #         - Do NOT add punctuation outside the JSON.
    #         - If you were not able to find a translation, just leave it blank, but always create a list of lists with three elements each, no more, no less

    #         Words: {words_list}
    #         """

    # response = ollama_model.respond_prompt(prompt)