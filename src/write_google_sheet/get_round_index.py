def get_round_index(bracketround):
    # Return the column of the round of the google sheets spreadsheet
    # (i.e. RD1 is column 3 of the table)
    round_values = {
        "first round": 3,
        "second round": 4,
        "sweet 16": 5,
        "elite eight": 6,
        "final four": 7,
        "championship": 8
    }

    return round_values[bracketround]