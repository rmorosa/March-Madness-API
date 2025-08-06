from src.mm_api_preprocessing.get_mm_data_from_api import get_mm_data_from_api
from src.mm_api_preprocessing.flatten_json import flatten_json
from src.mm_api_preprocessing.split_dict_by_games_id import split_dict_by_games_id
from src.mm_api_preprocessing.update_key_value import update_key_value
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from src.write_google_sheet.process_matches import process_matches
from src.write_google_sheet.update_strikethrough_counts import update_strikethrough_counts
import logging
import os
from dotenv import load_dotenv

load_dotenv()






# Pseudocode:
# 1. Function that returns march madness data for a specific day
# 2. Function that outputs that into pandas and a csv file
# 3. Function that does further processing to get just the game, teams, round, score, and winner
# 4. Functions that opens a file, writes to a different file based upon that data, and tallies points
# 5. Function that eliminates the team and updates teams left


csv_filename = "mm_data.csv"
csv_filtered_filename = "mm_filtered_data.csv"
split_word = "game_"
key = "bracketRound"
delimiter = "&" 

# Fetch mm data from api
mm_data = get_mm_data_from_api()

# Flatten data
flattened_mm_data = flatten_json(mm_data)

# Further process data to help put in pandas data frame format
processed_mm_data = split_dict_by_games_id(flattened_mm_data,split_word)

# Preprocess bracket Rounds that need it  (Sweet 16, Elite 8)
updated_key_vals = update_key_value(processed_mm_data,key,delimiter)

# Convert JSON data to a DataFrame
mm_df = pd.DataFrame(updated_key_vals)

# Save DataFrame to CSV
mm_df.to_csv(csv_filename, index = False)

# Filter columns by header value
mm_df_filtered = mm_df.filter(items=['gameID','gameState','away_names_short','home_names_short','home_winner','away_winner','bracketRound','home_seed','away_seed'])

# Save DataFrame to CSV
mm_df_filtered.to_csv(csv_filtered_filename, index = False)

# Convert DataFrame to a dictionary for easier lookup
df_dict = mm_df_filtered.to_dict(orient='records')

# only get games that are march madness from that day
filtered_df_dict = [d for d in df_dict if d.get("bracketRound") not in ("", None)]

# Define the scope
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(credentials_path)

# Authenticate using the credentials.json
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)
spreadsheet_id = "1my6p517Ij4BJyLeVLJe9dXy6tIS_Q3oaKY8gjhVXtLI"

# Open the Google Sheet
sheet = client.open_by_key(spreadsheet_id).sheet1  

# Get all values from the sheet
all_values = sheet.get_values()  # Returns a 2D list of all cell values

process_matches(sheet, all_values, filtered_df_dict)
update_strikethrough_counts(sheet, spreadsheet_id, creds)

logging.info("Script executed successfully.")



# Runs on thursdays through sundays every hour
# while True:
#     now = datetime.datetime.now()
#     if now.weekday() in [3, 4, 5, 6]:  # Thursday-Sunday
#         run_script()
#     time.sleep(900)  # Wait for 1 hour

