from src.write_google_sheet.find_table_headers import find_table_headers
from src.write_google_sheet.get_round_index import get_round_index
from src.write_google_sheet.get_bonus import get_bonus
from src.write_google_sheet.update_winner import update_winner
from src.write_google_sheet.update_loser import update_loser
import time
import random

def get_cell_value_with_retry(sheet, row, col, max_retries=5):
    """Fetch a cell value with exponential backoff in case of API failure."""
    retry_delay = 1  # Start with 1 second
    for attempt in range(max_retries):
        try:
            value = sheet.cell(row, col).value  # Attempt to get the cell value
            return value  # Return value if successful
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to fetch cell value ({row}, {col}). Error: {e}")
            if attempt < max_retries - 1:
                # backoff_time = (2 ** retries + random.uniform(0, 1)) * 2
                sleep_time = retry_delay * (2 ** attempt) + random.uniform(0, 1) * 2  # Add randomness to avoid collisions
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retries reached. Skipping this cell.")
                return None  # Return None if all retries fail


def process_matches(sheet, all_values, data_list):
    """Find matches in detected tables and update the sheet accordingly."""
    header_positions = find_table_headers(all_values,"Team")

    for row_start, col_start, headers in header_positions[:2]:
        for data in data_list:
            if data["gameState"].lower() != "final":
                print(f"Skipping match: {data['home_names_short']} vs {data['away_names_short']} (Status: {data['gameState']})")
                continue  # Skip if the game is not final

            home_name, away_name = data["home_names_short"].strip(), data["away_names_short"].strip()
            for row_idx in range(row_start + 1, len(all_values)):
                row = all_values[row_idx]

                if col_start < len(row) and row[col_start].strip() in [home_name, away_name]:
                    team_type = "home" if row[col_start].strip() == home_name else "away"
                    is_winner = data[f"{team_type}_winner"]
                    seed = data[f"{team_type}_seed"]
                    round_index = get_round_index(data["bracketRound"])
                    bonus = get_bonus(data["bracketRound"], is_winner)

                    # **Fetch the existing value with retry**
                    # existing_value = get_cell_value_with_retry(sheet, row_idx + 1, col_start + round_index)

                    # if existing_value:
                    #     print(f"Skipping update for {row[col_start]} at ({row_idx+1}, {col_start+round_index}) - Data already exists: {existing_value}")
                    #     continue  # Skip writing if data is present

                    if is_winner:
                        update_winner(sheet, row_idx, col_start, round_index, seed, bonus)
                    else:
                        update_loser(sheet, row_idx, col_start, round_index)