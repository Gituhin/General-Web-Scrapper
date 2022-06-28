from bs4 import BeautifulSoup
import requests
#from editor import g_sheets, auth_sheet
import sys
from googleapiclient.discovery import build
from google.oauth2 import service_account

def auth_sheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    creds = service_account.Credentials.from_service_account_file(
        'cred.json', scopes=SCOPES)

    sheet = build('sheets', 'v4', credentials=creds).spreadsheets()
    return sheet

class g_sheets:
    def __init__(self, doc, ID):
        self.ID = ID
        self.doc = doc

    def update(self, sheet, data):
        self.doc.values().update(spreadsheetId=self.ID,
                            range=f'{sheet}!D2', valueInputOption='USER_ENTERED',
                            body={'values':data}).execute()

    def append(self, sheet, data):
        self.doc.values().append(spreadsheetId=self.ID,
                                range=f'{sheet}!A1', valueInputOption='USER_ENTERED',
                                body={'values':data}).execute()

    def get(self, sheet, range):
        value = self.doc.values().get(spreadsheetId=self.ID,
                                    range=f'{sheet}!{range}').execute()
        try:                            
            return value['values'][0][0]
        except KeyError:
            return None


SPREADSHEET_ID = '1r7KF1rH-rjMz1k62qkgAxgZHUmaJj5XE5Huau64zLSc'

doc = auth_sheet()
file = g_sheets(doc, SPREADSHEET_ID)

WEBSITE = file.get('Crawler', 'B2')
w_sheet = file.get('Crawler', 'B3')
root, root_att = file.get('Crawler', 'B4'), eval(file.get('Crawler', 'D4'))
child, child_att = file.get('Crawler', 'B5'), eval(file.get('Crawler', 'D5'))
name, name_att = file.get('Crawler', 'B6'), eval(file.get('Crawler', 'D6'))
insti = file.get('Crawler', 'B7') 

if any(info is None for info in [WEBSITE, w_sheet, root, child, name]):
    file.update('Crawler', data=[['Info missing']])
    sys.exit()

print("Sending request to website...")
file.update('Crawler', data=[['Requesting Website...']])

try:
    webpage = requests.get(WEBSITE)
    con = BeautifulSoup(webpage.content, "lxml")
    file.update('Crawler', data=[['Request Successfull']])
except:
    file.update('Crawler', data=[['Some error with Website URL']])
    sys.exit()
print("Request successfull\n",'-----------')

values = []
try:
    main = con.find(root, root_att).findChildren(child, child_att)
except:
    file.update('Crawler', data=[['Some error in root tag']])
    sys.exit()

try:
    for u in main:
        facweb = u.find(name, name_att).a['href']
        fac_name = u.find(name, name_att).a.text
        rest =u.text
        values.append([fac_name, facweb, rest, insti])
except:
    file.update('Crawler', data=[['Some error in repetitive tag']])
    sys.exit()

print(len(values), "Rows appended")
file.update('Crawler', data=[['Appending Data']])
file.append(sheet=w_sheet, data=values)
file.update('Crawler', data=[[f'Data appended to {w_sheet}']])
