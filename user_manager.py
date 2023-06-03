import gspread
from oauth2client.service_account import ServiceAccountCredentials

class UserManager:
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("Flight Deals").worksheet("Users")
        self.empty_row = self.update_empty_row()
        self.emails = self.sheet.col_values(3)
        self.emails.pop(0)
    
    def create_new_user(self):
        print("Welcome to Jacob's Flight Club!")
        print("I find the BEST flight deals and email then straight to you!")
        f_name = input("What is your first name?\n")
        l_name = input("What is your last name?\n")
        email = "p"
        email_check = "s"
        while email != email_check:
            email = input("What is your email?\n")
            email_check = input("Type your email in again.\n")
        print("You're in the club!")
        
        self.sheet.update_cell(self.empty_row, 1, f"{f_name}")
        self.sheet.update_cell(self.empty_row, 2, f"{l_name}")
        self.sheet.update_cell(self.empty_row, 3, f"{email}")
        self.empty_row += 1
    
    def update_empty_row(self):
        empty_cell = self.sheet.cell(1, 1).value
        row = 1
        while empty_cell != None:
            row += 1
            empty_cell = self.sheet.cell(row, 1).value
        return row

