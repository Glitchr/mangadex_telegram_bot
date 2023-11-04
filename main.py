import json, time

import Chapter, Manga, User, utils, api


# Set an interval for checking the feed (in seconds)
interval = 60

# Set a file name for storing the feed data
file_name = 'feed_data.json'

# Create a payload with the user credentials
payload = {'username': api.USER, 'password': api.PASS}

# Authenticate to the mangadex API and get the header
header = api.api_auth(payload)
 
# Try to load the feed data from the file, if it exists
try:
    with open(file_name, "r") as f:
        previous_feed = json.load(f)
except FileNotFoundError:
    previous_feed = {}

while True:
    # Get the current feed data from the mangadex API
    current_feed = api.get_latest_manga_feed(header)
    # Compare the current feed data with the previous feed data
    for chapter_id in current_feed:
        # If the chapter_id is not in the previous feed data, it means it is a 
        # new chapter
        if chapter_id not in previous_feed:
            # Get the chapter_info from the current feed data
            chapter_info = current_feed[chapter_id]
            # Print out the new chapter in a readable format
            print(utils.readable_chapter(chapter_info))
    # Update the previous feed data with the current feed data
    previous_feed = current_feed
    # Save the feed data to the file
    with open(file_name, "w") as f:
        json.dump(previous_feed, f)
    # Wait for the interval before checking again
    time.sleep(interval)
