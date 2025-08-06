import pandas as pd

def json_to_csv(json_data, csv_filename):
    """
    Converts JSON data to a CSV file.

    Parameters:
    json_data (list or dict): The JSON data to convert, typically a list of dictionaries.
    csv_filename (str): The name of the CSV file to save the data.

    Returns:
    pd.DataFrame: The DataFrame created from the JSON data.
    """

    # Convert JSON data to a DataFrame
    df = pd.DataFrame(json_data)

    # Drop rows where all values are NaN
    df.dropna(how='all', inplace=True)

    # Save DataFrame to CSV
    df.to_csv(csv_filename, index=False)
    
    return df