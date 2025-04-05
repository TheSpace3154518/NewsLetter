from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

SERVICE_ACCOUNT_FILE = 'Google-Key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_emails():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    SPREADSHEET_ID = '1KG3PyKvAvsdKJYFQFFc8r3IOA4aFOapzd2_0tBIUoCs'

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='A:ZZ').execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

print(get_emails())