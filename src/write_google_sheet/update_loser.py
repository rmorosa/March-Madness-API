import string
from src.write_google_sheet.get_num_of_zeros import get_num_of_zeros
import time
import random

def update_loser(sheet, row_idx, col_start, round_index):
    """Strikethrough losing team and add zeros to the rest of the row in a batch request."""

    team_col_letter = string.ascii_uppercase[col_start] 
    cell = f"{team_col_letter}{row_idx + 1}"

    # ✅ Step 2: Get the number of zeros to insert
    num_of_zeros = get_num_of_zeros(round_index)

    # ✅ Step 3: Construct batch update requests
    col_start_index = col_start + round_index
    col_end_index = col_start_index + num_of_zeros

    # Convert column index to letter format
    def col_letter(idx):
        """Convert column index to Excel-style letters (A, B, ..., Z, AA, AB, etc.)."""
        result = ""
        while idx >= 0:
            result = chr(idx % 26 + 65) + result
            idx = idx // 26 - 1
        return result

    start_col_letter = col_letter(col_start_index - 1)
    end_col_letter = col_letter(col_end_index - 1)  # -1 because end index is exclusive
    zero_range = f"{start_col_letter}{row_idx + 1}:{end_col_letter}{row_idx + 1}"

    # Prepare the zero values list for batch update
    zero_values = [[0] * num_of_zeros]  # List of lists for batch update

    # ✅ Step 3: Clean and Validate Range
    def clean_range(range_str):
        """Ensure the range is properly formatted (prevents duplicate sheet names)."""
        if "!" in range_str:
            parts = range_str.split("!")
            return parts[-1]  # Keep only the cell range without sheet name
        return range_str  # Return as is if no issue

    # ✅ Step 3: Construct batch update requests
    values_request = [
        {"range": clean_range(zero_range), "values": [[0] * num_of_zeros]}  # Insert zeros
    ]

    # ✅ Step 4: Construct formatting request (must be sent separately)
    formatting_request = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet.id,  # Sheet ID required for formatting updates
                        "startRowIndex": row_idx,
                        "endRowIndex": row_idx + 1,
                        "startColumnIndex": col_start,
                        "endColumnIndex": col_start + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {"strikethrough": True}
                        }
                    },
                    "fields": "userEnteredFormat.textFormat.strikethrough"
                }
            }
        ]
    }
   
    # ✅ Step 5: Batch update values with retry logic
    def batch_update_with_retry(sheet, values_request, formatting_request, max_retries=10):
        retries = 0
        while retries < max_retries:
            try:
                # ✅ Clean ranges before retrying
                cleaned_values_request = [
                    {"range": clean_range(val["range"]), "values": val["values"]}
                    for val in values_request
                ]
                # Send batch update for values
                sheet.batch_update(cleaned_values_request)

                # Send batch update for formatting separately
                sheet.spreadsheet.batch_update(formatting_request)

                print("Batch update successful.")
                return
            except Exception as e:
                if "429" in str(e):
                    retries += 1
                    backoff_time = (2 ** retries + random.uniform(0, 1)) * 2
                    print(f"Rate limit exceeded. Retrying in {backoff_time:.2f} seconds...")
                    time.sleep(backoff_time)
                else:
                    raise e  # Raise other errors

    batch_update_with_retry(sheet, values_request, formatting_request)
