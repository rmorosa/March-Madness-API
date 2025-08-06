from src.mm_api_preprocessing.get_games_id import get_games_id
import pytest

@pytest.fixture
def underscore():
    return '_'

def test_get_groups_identifier_success(underscore):
    key = 'jimmy_neutron_boy_genius'
    delimiter = underscore

    assert delimiter == "_"

    games_id = get_games_id(key,delimiter)

    assert games_id == "jimmyneutron"

def test_get_groups_identifier_failure(underscore):
    key = 'jimmyneutronboygenius'
    delimiter = underscore

    assert delimiter == "_"

    games_id = get_games_id(key,delimiter)

    assert games_id == "There is no delimiter in the key"