import json, time
from decouple import config
from utils import readable_chapter, retry_on_failure
from api import api_auth, api_token_refresh, get_latest_manga_feed
from handler import send_chapter


interval = 60 # Set an interval for checking the feed (1 minute in seconds)

# Set a file name for storing the feed data
file_name = 'feed_data.json'

# Create a payload with the user credentials
payload = {
    'grant_type': 'password',
    'username': config('M_USER'),
    'password': config('PASS'),
    'client_id': config('CLIENT_ID'),
    'client_secret': config('CLIENT_SECRET'),
    }
            
# Authenticate to the mangadex API and get the header
header, refresh_token = retry_on_failure(api_auth, payload)

# Try to load the feed data from the file, if it exists
try:
    with open(file_name, "r") as f:
        previous_feed = json.load(f)
except FileNotFoundError:
    previous_feed = {}

while True:
    # Get the current feed data from the mangadex API
    try:
        current_feed = get_latest_manga_feed(header)
    except Exception as e:
        # If the exception is caused by a 401 response, refresh the header and retry
        if str(e) == 'Retrieval failed: 401':
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': config('CLIENT_ID'),
                'client_secret': config('CLIENT_SECRET')
            }
            header, refresh_token = retry_on_failure(api_token_refresh, payload)
            current_feed = get_latest_manga_feed(header)
        # If the exceptions is caused by something else, raise it
        else:
            raise e

    # Compare the current feed data with the previous feed data
    for chapter_id in current_feed:
        # If the chapter_id is not in the previous feed data, it means it is a 
        # new chapter
        if chapter_id not in previous_feed:
            # Get the chapter_info from the current feed data
            chapter_info = current_feed[chapter_id]
            print(readable_chapter(chapter_info))
            send_chapter(readable_chapter(chapter_info))
    # Update the previous feed data with the current feed data
    previous_feed = current_feed
    # Save the feed data to the file
    with open(file_name, "w") as f:
        json.dump(previous_feed, f)
    # Wait for the interval before checking again
    time.sleep(interval)
