import pytest
import pandas as pd
from src.mm_api_preprocessing.split_dict_by_games_id import split_dict_by_games_id

@pytest.fixture
def sample_data():
    """Fixture for providing sample JSON data."""
    return {"games_0_game_id": 1, "games_0_game_name": "Alice", "games_0_game_age": 30, 
            "igloo": 2, "football": "Bob", "dog": 25,
            "games_2_game_id": 3, "games_2_game_name": "Charlie", "games_2_game_age": 35},"game_"


def test_split_dict_by_games_id(sample_data):

    games_dic,split_word = sample_data

    dict_list = split_dict_by_games_id(games_dic,split_word)

    # Check second dictionary doesnt exist in result and the length becomes 2
    assert len(dict_list) == 2
    # Check key is stripped properly
    assert "id" in dict_list[0]
    assert "name" in dict_list[0]
    assert "age" in dict_list[0]
    # Check key kept its value
    assert dict_list[0]["id"] == 1
    assert dict_list[0]["name"] == "Alice"
    assert dict_list[0]["age"] == 30
