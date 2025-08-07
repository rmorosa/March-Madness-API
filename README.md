# March-Madness-API
The backend of March Madness with a twist that handles API requests and responses.

# Prerequisites
## Setup: Google Sheets API Credentials
To use this project, you’ll need to create your own Google Cloud Service Account and download a credentials.json file:

1. Go to Google Cloud Console

1. Create or select a project

1. Enable the Google Sheets API

1. Go to IAM & Admin > Service Accounts

1. Click Create Service Account

1. Give it a name (e.g., sheets-api)

1. After creation, click the new service account → Keys > Add Key > Create New Key (JSON)

1. Save the credentials.json file in your project directory

1. Share your target Google Sheet with the service account email (it looks like something@your-project.iam.gserviceaccount.com)

1. Give Editor access since script writes data
1. Set the environment variable in your .env file following the .env.example

## Other Setup Instructions
1. Ensure you install all dependencies with the following command `pip install requirements.txt`
1. Ensure you are opened to [file](https://docs.google.com/spreadsheets/d/1my6p517Ij4BJyLeVLJe9dXy6tIS_Q3oaKY8gjhVXtLI/edit?gid=0#gid=0) and all data from rounds 1 through 6 is cleared for each person and no teams are crossed out

# To Run:
1. In the root of March-Madness-API you can run `python main.py` which then does the following:
    - The first function returns march madness data for a specific day
        - You can change the month and day for the url within the get_mm_data_from_api function to get data for a different date
    - The next series of functions do a ton of pre-processing to get just the game, teams, round, score, and winner
    - There is then a series of functions that opens a [file](https://docs.google.com/spreadsheets/d/1my6p517Ij4BJyLeVLJe9dXy6tIS_Q3oaKY8gjhVXtLI/edit?gid=0#gid=0), writes to it based upon the pre-processed data, and tallies points for each person
    - There is a final function that eliminates the team if they lost and updates teams left

# Follow-On Tasks
    - You can change the month and day for the url within the get_mm_data_from_api function to get data for a different date (i.e. Change to https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2025/03/21 after computing https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2025/03/20)
    - You will see the scoreboard gets populated in real time
    - During March Madness, this script gets ran Thursday through Sunday every hour using a simple loop
