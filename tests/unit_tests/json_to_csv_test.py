# import pytest
# import pandas as pd
# from src.json_to_csv import json_to_csv

# @pytest.fixture
# def sample_json_data():
#     """Fixture for providing sample JSON data."""
#     return [
#         {"id": 1, "name": "Alice", "age": 30},
#         {"id": 2, "name": "Bob", "age": 25},
#         {"id": 3, "name": "Charlie", "age": 35}
#     ]

# def test_json_to_csv(sample_json_data, tmp_path):
#     # Create a temporary file path
#     csv_file = tmp_path / "output.csv"
    
#     # Call the function with sample JSON data and the temporary file path
#     df = json_to_csv(sample_json_data, csv_file)
    
#     # Check if the CSV file is created
#     assert csv_file.exists()
    
#     # Read the CSV file back into a DataFrame
#     df_read = pd.read_csv(csv_file)
    
#     # Check if the data matches the original JSON data
#     assert df.equals(df_read)

# def test_json_to_csv_empty_data(tmp_path):
#     # Test with empty JSON data
#     csv_file = tmp_path / "empty_output.csv"
#     empty_json_data = []
    
#     df = json_to_csv(empty_json_data, csv_file)
    
#     # Check if the CSV file is created
#     assert csv_file.exists()
    
#     # Check if the DataFrame is empty
#     assert df.empty