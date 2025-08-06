def count_strikethroughs_by_header(sheet_data, header_name):
    print("sheet_data:")
    print(sheet_data)
    strikethrough_counts = []
    header_indices = []
    header_teams_left_indices = []

    # Step 1: Find all occurrences of the header
    for row_index, row in enumerate(sheet_data):
        if "values" in row:
            for col_index, cell in enumerate(row["values"]):
                if "effectiveValue" in cell and cell["effectiveValue"].get("stringValue", "") == header_name:
                    header_indices.append((row_index, col_index))  # Store (row, col) of the header
                elif "effectiveValue" in cell and cell["effectiveValue"].get("stringValue", "") == "Teams Left":
                    header_teams_left_indices.append((row_index, col_index))  # Store (row, col) of the header

    # Step 2: For each header occurrence, process the table under it
    for header_row, header_col in header_indices:
            
        strikethrough_count = 0
        current_row = header_row + 1  # Start checking from the row below the header

        while current_row < len(sheet_data):
            row = sheet_data[current_row]
            if "values" in row and len(row["values"]) > header_col:
                cell = row["values"][header_col]

                # Stop processing if the cell is empty
                if "effectiveValue" not in cell:
                    break

                # Check for strikethrough formatting
                if "userEnteredFormat" in cell:
                    text_format = cell["userEnteredFormat"].get("textFormat", {})
                    if text_format.get("strikethrough", False):
                        strikethrough_count += 1
            else:
                break

            current_row += 1

        strikethrough_counts.append(strikethrough_count)
    
    # Update each tuple by appending the value from the second list
    for i, value in enumerate(strikethrough_counts):
        print("value:")
        print(value)
        header_teams_left_indices[i] = header_teams_left_indices[i] + (value,)

    if len(header_indices) == 0:
        return []
    else:
        return header_teams_left_indices