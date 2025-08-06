import requests
from datetime import datetime

def get_mm_data_from_api():
    """
    Fetches data from the given NCAA API endpoint.
    
    :return: Response JSON data or raises an exception if the request fails
    """
    # Get current date in YYYY/MM/DD format
    # current_date = datetime.now().strftime("%Y/%m/%d")

    # url = f"https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/{current_date}"

    url = "https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2025/03/20"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) # Terminates the program
