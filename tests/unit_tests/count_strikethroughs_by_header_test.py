import pytest
from src.write_google_sheet.count_strikethroughs_by_header import count_strikethroughs_by_header  # Import your function

def test_single_header_with_strikethroughs():
    # Mock Google Sheets API response
    sheet_data = [
        {"values": [{"effectiveValue": {"stringValue": "Header1"}}, {"effectiveValue": {"stringValue": "Teams Left"}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data1"}, "userEnteredFormat": {"textFormat": {"strikethrough": True}}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data2"}, "userEnteredFormat": {"textFormat": {"strikethrough": False}}}]},
    ]
    
    result = count_strikethroughs_by_header(sheet_data, "Header1")

    assert result == [(0, 1, 1)]  # Expected format: (row, col, strikethrough_count)

def test_multiple_headers_with_strikethroughs():
    # Mock Google Sheets API response
    sheet_data = [
        {"values": [{"effectiveValue": {"stringValue": "Header1"}}, {"effectiveValue": {"stringValue": "Teams Left"}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data1"}, "userEnteredFormat": {"textFormat": {"strikethrough": True}}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data2"}, "userEnteredFormat": {"textFormat": {"strikethrough": False}}}]},
        {"values": [{"effectiveValue": {"stringValue": "Header1"}}, {"effectiveValue": {"stringValue": "Teams Left"}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data1"}, "userEnteredFormat": {"textFormat": {"strikethrough": True}}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data2"}, "userEnteredFormat": {"textFormat": {"strikethrough": False}}}]},
    ]
    
    result = count_strikethroughs_by_header(sheet_data, "Header1")

    assert result == [(0, 1, 2),(3,1,1)]  # Expected format: (row, col, strikethrough_count)

def test_header_name_not_existing():
    # Mock Google Sheets API response
    sheet_data = [
        {"values": [{"effectiveValue": {"stringValue": "Header1"}}, {"effectiveValue": {"stringValue": "Teams Left"}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data1"}, "userEnteredFormat": {"textFormat": {"strikethrough": True}}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data2"}, "userEnteredFormat": {"textFormat": {"strikethrough": False}}}]},
        {"values": [{"effectiveValue": {"stringValue": "Header1"}}, {"effectiveValue": {"stringValue": "Teams Left"}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data1"}, "userEnteredFormat": {"textFormat": {"strikethrough": True}}}]},
        {"values": [{"effectiveValue": {"stringValue": "Data2"}, "userEnteredFormat": {"textFormat": {"strikethrough": False}}}]},
    ]
    
    result = count_strikethroughs_by_header(sheet_data, "No header")

    assert result == []  # Expected format: (row, col, strikethrough_count)