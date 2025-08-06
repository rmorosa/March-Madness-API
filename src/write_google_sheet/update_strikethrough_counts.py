import time
import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.write_google_sheet.count_strikethroughs_by_header import count_strikethroughs_by_header

def update_strikethrough_counts(sheet, spreadsheet_id, creds, max_retries=5):
    """Fetch data and update the count of strikethrough teams using batch update with backoff."""
    service = build("sheets", "v4", credentials=creds)

    retries = 0
    while retries < max_retries:
        try:
            # ✅ Step 1: Fetch spreadsheet data with only necessary fields
            response = service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                fields="sheets.data.rowData.values.userEnteredFormat.textFormat.strikethrough,"
                       "sheets.data.rowData.values.effectiveValue"
            ).execute()

            # ✅ Step 2: Extract sheet data and count strikethroughs
            sheet_data = response['sheets'][0]['data'][0]['rowData']
            results = count_strikethroughs_by_header(sheet_data, "Team")

            # ✅ Step 3: Prepare batch update requests
            update_requests = []
            for header_row, teams_left_column_index, count in results:
                update_requests.append({
                    "updateCells": {
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": header_row + 1,
                            "endRowIndex": header_row + 2,
                            "startColumnIndex": teams_left_column_index,
                            "endColumnIndex": teams_left_column_index + 1
                        },
                        "rows": [
                            {
                                "values": [
                                    {"userEnteredValue": {"formulaValue": f"=8-{count}"}}
                                ]
                            }
                        ],
                        "fields": "userEnteredValue"
                    }
                })

            # ✅ Step 4: Send batch update
            if update_requests:
                batch_body = {"requests": update_requests}
                service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_body).execute()

            print("✅ Strikethrough count update successful.")
            return  # Exit on success

        except HttpError as e:
            if e.resp.status == 429:  # Handle rate limit exceeded error
                retries += 1
                backoff_time = (2 ** retries + random.uniform(0, 1)) * 3  # Exponential backoff
                print(f"⚠️ Rate limit exceeded. Retrying in {backoff_time:.2f} seconds...")
                time.sleep(backoff_time)
            else:
                raise e  # Raise other errors immediately
