"""
1. pip install gspread
2. pip install oauth2client 
3. Go to https://console.developers.google.com
4. Create project
5. App below APIs
    -> Google drive
    -> Google sheets API
6. Add credentials 
7. Share the sheet with the email address in the client_secret.json
8. Access data from your python script"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive', 
        'https://spreadsheets.google.com/feeds']

creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)
sheet = client.open('demo_sheet').sheet1
sheet.append_row(["Row3","Row4"])
print(dir(sheet))
sheet.spreadsheet.add_worksheet("sheet2",5,5)
sheet_data = sheet.get_all_records()
print(sheet_data)