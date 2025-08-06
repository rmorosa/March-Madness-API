import pytest
import pandas as pd
from src.mm_api_preprocessing.flatten_json import flatten_json

@pytest.fixture
def sample_json_data():
    """Fixture for providing sample JSON data."""
    return  {
        "user": {
            "id": 123,
            "name": "John",
            "address": {
                "city": "New York",
                "zip": "10001"
            }
        },
        "orders": [
            {"id": 1, "item": "Laptop"},
            {"id": 2, "item": "Phone"}
        ]
    }

def test_flatten_json(sample_json_data):
    flattened_data = flatten_json(sample_json_data)
    
    # Check nested dictionary is flattened correctly
    assert "user_id" in flattened_data 
    assert flattened_data["user_id"] == 123

    # Check nested list is flattened correctly
    assert "orders_0_id" in flattened_data 
    assert flattened_data["orders_0_id"] == 1