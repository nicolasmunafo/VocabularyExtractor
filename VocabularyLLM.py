import requests
from pathlib import Path
from PIL import Image
import base64
from typing import List
import ast

class AIModel():
    def __init__(self):
        pass

    def respond_prompt(self, prompt_text: str) -> List[List[str]]:
        prompt = """Can you translate these German words in Spanish and English? Lernziele, Ausbildung, Zollinhaltserklärung. 
        Just with one or two short translations of each word.
        Can you also write the results as python lists, [[word1, translation spanish, translation english], [word2, translation spanish, translation english]]"""

        ollama_url = 'http://localhost:11434/api/generate'
        
        payload = {
            "model": "phi3",
            "prompt": prompt_text,
            "stream": False
        }

        response = requests.post(ollama_url, json=payload)   
        return ast.literal_eval(response.json()["response"])     
        return response.json()["response"]


# pil_img =Image.open("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/Images/Lektion 1/IMG_4232.JPG")#.convert('RGB')
path_img = Path("C:/Users/Nicolas/GitHub/Automation_Py/VocabularyExtractor/Images/Lektion 1/IMG_4231.JPG")
# Load image and encode to base64
with open(path_img, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()


# prompt = """This is a page from a German vocabulary textbook with a 3-column layout: 
# German word, handwritten translation, example sentence. 
# Ignore any furniture diagrams, sticky notes, or unrelated header/footer text.
# Return only the vocabulary entries as a list in the format:
# German word | translation | example sentence"""

# payload = {
#     "model": "llama3.2-vision",
#     "prompt": prompt,
#     "images": [img_b64],
#     "stream": False
# }
