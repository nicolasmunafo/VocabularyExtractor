import json
from pathlib import Path

class ConfigReader:
    def __init__(self):
        self._gsheets_credential = ""
        self._sheet_id = ""
        self._ollama_url = ""
        self._images_path = ""
        self._config_file = Path(__file__).parent / "config.json" 
        self.__read_config()

    def __read_config(self):
        json_file = ""
        
        try:
            with open(self._config_file, "r") as f:
                json_file = json.load(f)
        except FileNotFoundError:
            print("Config file not found")
            return
        
        self._gsheets_credential = json_file["gsheets_credential"]
        self._sheet_id = json_file["sheet_id"]
        self._ollama_url = json_file["ollama_url"]
        self._images_path = json_file["images_path"]
    
    @property
    def gsheets_credential(self):
        return self._gsheets_credential
    
    @property
    def sheet_id(self):
        return self._sheet_id
    
    @property
    def ollama_url(self):
        return self._ollama_url
      
    @property
    def images_path(self):
        return self._images_path

        






