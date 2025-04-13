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

def delete_emails_by_ids():
    try:
        # Setup Google Sheets API
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(
            'Google-Key.json', scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        IDS_SPREADSHEET_ID = '1FPtRZQFTURjyEE-ht_4uwwcqCZdBmaOH5UkQphUN7QA'
        EMAILS_SPREADSHEET_ID = '1KG3PyKvAvsdKJYFQFFc8r3IOA4aFOapzd2_0tBIUoCs'

        # Get IDs to delete
        result = service.spreadsheets().values().get(
            spreadsheetId=IDS_SPREADSHEET_ID, range='A:ZZ').execute()
        ids_to_delete = [row[1] for row in result.get('values', [])[1:]]

        # Get emails data
        result = service.spreadsheets().values().get(
            spreadsheetId=EMAILS_SPREADSHEET_ID, range='A:ZZ').execute()
        headers = result.get('values', [])[0]
        rows = result.get('values', [])[1:]

        # Filter out rows with matching IDs
        id_index = headers.index('Id')
        updated_rows = [row for row in rows if row[id_index] not in ids_to_delete]

        # Get sheet ID first
        sheet_metadata = service.spreadsheets().get(spreadsheetId=EMAILS_SPREADSHEET_ID).execute()
        sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']

        # Clear existing content
        request_body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "ROWS",
                            "startIndex": 1,
                            "endIndex": len(rows) + 1
                        }
                    }
                }
            ]
        }
        service.spreadsheets().batchUpdate(
            spreadsheetId=EMAILS_SPREADSHEET_ID,
            body=request_body
        ).execute()

        # Update with new content
        body = {
            'values': [headers] + updated_rows
        }
        service.spreadsheets().values().update(
            spreadsheetId=EMAILS_SPREADSHEET_ID, range='A:ZZ',
            valueInputOption='RAW', body=body).execute()

        # Get sheet ID for IDs spreadsheet
        ids_sheet_metadata = service.spreadsheets().get(spreadsheetId=IDS_SPREADSHEET_ID).execute()
        ids_sheet_id = ids_sheet_metadata['sheets'][0]['properties']['sheetId']

        # Clear IDs spreadsheet
        request_body = {
            "requests": [
            {
                "deleteDimension": {
                "range": {
                    "sheetId": ids_sheet_id,
                    "dimension": "ROWS",
                    "startIndex": 1,
                    "endIndex": len(ids_to_delete) + 1
                }
                }
            }
            ]
        }
        result = service.spreadsheets().batchUpdate(
            spreadsheetId=IDS_SPREADSHEET_ID,
            body=request_body
        ).execute()

        print(f"Successfully deleted {len(rows) - len(updated_rows)} emails")
        return True

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False
