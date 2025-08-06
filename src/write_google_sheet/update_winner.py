import time
import random

def update_winner(sheet, row_idx, col_start, round_index, seed, bonus):
    """Update the winning team’s seed and bonus points using batch update with exponential backoff."""

    threshold_round = 6

    bonus_col_index = col_start + 9  # Column index for bonus
    seed_col_index = col_start + round_index  # Column index for seed

    # Convert column index to letter (A-Z, AA-ZZ, etc.)
    def col_letter(idx):
        """Convert column index (0-based) to letter (e.g., 0 -> 'A', 25 -> 'Z', 26 -> 'AA')"""
        result = ""
        while idx >= 0:
            result = chr(idx % 26 + 65) + result
            idx = idx // 26 - 1
        return result

    bonus_col_letter = col_letter(bonus_col_index - 1)
    seed_col_letter = col_letter(seed_col_index - 1)

    # Define cell range
    cell_range = f"{bonus_col_letter}{row_idx + 1}"

    # Function to perform batch_get with retries
    def batch_get_with_retry(sheet, cell_range, max_retries=5):
        """Attempt batch_get with exponential backoff to avoid rate limits."""
        retries = 0
        while retries < max_retries:
            try:
                result = sheet.batch_get([cell_range])
                return result  # Success
            except Exception as e:
                if "429" in str(e):  # Handle rate limits
                    retries += 1
                    backoff_time = (2 ** retries + random.uniform(0, 1)) * 2  # Exponential backoff
                    print(f"Rate limit exceeded. Retrying batch_get in {backoff_time:.2f} seconds...")
                    time.sleep(backoff_time)
                else:
                    raise e  # Raise other exceptions

        print("Max retries reached. Could not fetch data.")
        return None  # Return None if all retries fail

    # ✅ Get current bonus value with retries
    bonus_values = batch_get_with_retry(sheet, cell_range)

    try:
        if bonus_values and isinstance(bonus_values, list):
            # Flatten nested list properly
            raw_value = bonus_values[0]
            while isinstance(raw_value, list) and len(raw_value) > 0:
                raw_value = raw_value[0]  # Keep extracting until we get a string/number
            
            # Convert to int safely, handle empty cases
            current_bonus_value = int(raw_value) if raw_value else 0
        else:
            current_bonus_value = 0  # Default if empty or incorrect format
    except (IndexError, ValueError, TypeError) as e:
        print("DEBUG: Error converting to int:", e, "Raw data:", bonus_values)
        current_bonus_value = 0  # Fallback to zero if there's an issue


    # ✅ If below the threshold round, bonus stays at 0
    if round_index < threshold_round:
        updated_bonus_value = 0
    else:
        updated_bonus_value = current_bonus_value + bonus

    print("updated_bonus_value:", updated_bonus_value)

    # ✅ If below the threshold round, bonus stays at 0
    # if round_index < threshold_round:
    #     updated_bonus_value = 0
    # else:
    #     # ✅ Correcting the bonus progression to be 3 → 9 → 18
    #     if current_bonus_value == 3:
    #         updated_bonus_value = 9
    #     elif current_bonus_value == 9:
    #         updated_bonus_value = 18
    #     elif current_bonus_value == 18:
    #         updated_bonus_value = 18  # No change needed
    #     else:
    #         updated_bonus_value = 3  # Default for first-time updates

    # print("updated_bonus_value:", updated_bonus_value)

    print("DEBUG: current_bonus_value =", current_bonus_value)
    print("bonus:", bonus)

    # Skip update if bonus is already correct
    if (current_bonus_value, bonus) in [(3, 3), (9, 6), (18, 9)]:
        return  

    # updated_bonus_value = bonus + current_bonus_value
    # print("updated_bonus_value:", updated_bonus_value)

    # Batch update values
    values = [
        {"range": f"{seed_col_letter}{row_idx + 1}", "values": [[int(seed)]]},
        {"range": f"{bonus_col_letter}{row_idx + 1}", "values": [[updated_bonus_value]]}
    ]

    # Debugging: Print the exact range being passed for batch_update
    for val in values:
        print(f"DEBUG: range = {val['range']}, values = {val['values']}")

    # Function to clean range strings (remove extra sheet names)
    def clean_range(range_value):
        """Remove any sheet name prefixes from the range."""
        if "'" in range_value:
            parts = range_value.split("'")
            if len(parts) > 2:
                range_value = "'".join(parts[2:])
        return range_value

    # Function to attempt batch update with exponential backoff
    def batch_update_with_retry(values, max_retries=5):
        """Attempt batch update with retries using exponential backoff."""
        retries = 0
        while retries < max_retries:
            try:
                # Clean all ranges before retrying to avoid appending sheet name
                cleaned_values = [
                    {"range": clean_range(val["range"]), "values": val["values"]}
                    for val in values
                ]

                print(f"Retrying batch update with values: {cleaned_values}")
                sheet.batch_update(cleaned_values)  # Perform batch update
                print("Batch update successful.")
                return  # Success
            except Exception as e:
                if "429" in str(e):  # Handle rate limits
                    retries += 1
                    backoff_time = (2 ** retries + random.uniform(0, 1)) * 2  # Exponential backoff + jitter
                    print(f"Rate limit exceeded. Retrying batch_update in {backoff_time:.2f} seconds...")
                    time.sleep(backoff_time)
                else:
                    raise e  # Raise other exceptions

        print("Max retries reached. Could not complete the batch update.")

    # ✅ Perform batch update with retry logic
    batch_update_with_retry(values)
