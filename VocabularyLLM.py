import requests
from pathlib import Path
from typing import List
import ollama
from pydantic import BaseModel
import json
import ast

# To create a JSON schema as a format for the response
class WordTranslation(BaseModel):
    translations: List[List[str]]
    # spanish_translation: str
    # english_translation: str

class AIModel():
    def __init__(self, ollama_url: str):
        self._ollama_url = ollama_url

    def respond_prompt(self, prompt_text: str) -> List[List[str]]:
        ollama_url = self._ollama_url
        
        payload = {
            "model": "phi3",
            "prompt": prompt_text,
            "stream": False
        }

        response = requests.post(ollama_url, json=payload)

        # To convert the response into a literal Python list
        # return ast.literal_eval(response.json()["response"])
        return response.json()["response"]
    
    
    def respond_prompt_list(self, prompt_text: str) -> List[List[str]]:
        response = ollama.chat(
            model='phi3',
            messages=[
                {
                    'role': 'user',
                    'content': f'{prompt_text}'
                }
            ],
            format=WordTranslation.model_json_schema(),
            options={
                'temperature': 0.0  # Crucial: Makes the model deterministic
            }

        )

        try:
            raw_content = response["message"]["content"]
            translations = json.loads(raw_content)
        except Exception as e:
            print(f"Parsing error: {e}")
        return translations