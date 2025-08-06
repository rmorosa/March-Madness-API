def find_table_headers(all_values, header_name):
    """Detect multiple tables by searching for header positions."""
    header_positions = []
    for row_idx, row in enumerate(all_values):
        for col_idx, cell in enumerate(row):
            if cell == header_name:
                headers = all_values[row_idx][col_idx:]  # Extract headers
                header_positions.append((row_idx, col_idx, headers))
    return header_positions