import requests
from pathlib import Path
import base64
from typing import List
import ast

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
        return ast.literal_eval(response.json()["response"])
