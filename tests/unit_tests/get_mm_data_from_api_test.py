import pytest
import requests_mock
from src.mm_api_preprocessing.get_mm_data_from_api import get_mm_data_from_api

@pytest.fixture
def sample_url():
    # Setup code
    endpoint_url = 'https://api.example.com/data'
    return endpoint_url

def test_get_data_from_api_success(sample_url):
    assert sample_url == 'https://api.example.com/data'
    mock_data = {'key': 'value'}
    with requests_mock.Mocker() as m:
        # Mock the GET request and specify the JSON response
        m.get(sample_url, json=mock_data)

        # Call the function being tested
        result = get_mm_data_from_api(sample_url)
        
        # Assert that the result matches the expected mock data
        assert result == mock_data
        assert m.called_once

def test_get_data_from_api_failure(sample_url):
    assert sample_url == 'https://api.example.com/data'
    with requests_mock.Mocker() as m:
        # Mock the GET request and specify a 404 error
        m.get(sample_url, status_code=404)
        
        # Assert that SystemExit is raised
        with pytest.raises(SystemExit):
            get_mm_data_from_api(sample_url)