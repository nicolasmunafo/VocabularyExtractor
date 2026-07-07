from typing import List
from pathlib import Path
from config.config_reader import ConfigReader
import gspread


class GSheetManager:
    def __init__(self):
        pass

    def save_contents_file(self, words_list: List[List[str]], config_reader: ConfigReader, level: str, lektion: str) -> None:
        
        # Get credentials, spreadsheet ID and get spreadsheet
        credentials_path = Path.cwd() / config_reader.gsheets_credential
        sheet_id = config_reader.sheet_id[level]
        gc = gspread.service_account(filename=credentials_path)
        sh = gc.open_by_key(sheet_id)

        # If sheet doesn't exist, create it
        if not(self.check_existing_sheet(lektion, sh)):
            self.create_sheet(lektion, sh)

        sh.worksheet(lektion).append_rows(words_list)


    def check_existing_sheet(self, sheet_name: str, spreadsheet: gspread.Spreadsheet) -> bool:
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except Exception as e:
            return False        
        return True


    def create_sheet(self, sheet_name: str, spreadsheet: gspread.Spreadsheet) -> None:
        spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=10)