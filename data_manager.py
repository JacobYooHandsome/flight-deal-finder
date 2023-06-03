import gspread
from oauth2client.service_account import ServiceAccountCredentials

class DataManager:
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("Flight Deals").sheet1
        self.cities = self.sheet.col_values(1)
        self.cities.pop(0)
        self.prices = self.sheet.col_values(3)
        self.prices.pop(0)

    def update_IATAs(self, codes):
        row = 2
        for code in codes:
            if self.sheet.cell(row, 2).value == None:
                self.sheet.update_cell(row, 2, f"{code}")
            row += 1
        