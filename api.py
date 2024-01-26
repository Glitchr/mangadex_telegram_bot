"""This module handles all of the API calls to Mangadex"""

import requests
from log import logger

# Define some constants for the mangadex API
BASE_URL = "https://api.mangadex.org"
AUTH_URL = "https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token"
FEED_URL = "https://api.mangadex.org/user/follows/manga/feed"
FEED_PARAMS = {
    "limit": 50,
    "translatedLanguage[]": ["en", "es-la"],
    "order[updatedAt]": "desc",
    "order[volume]": "desc",
    "order[chapter]": "desc",
    "includes[]": "manga",
}


def api_auth(payload):
    """Authenticate to the mangadex API and return the header"""
    try:
        auth = requests.post(AUTH_URL, data=payload)
        if auth.status_code == 200:
            auth_json = auth.json()
            access_token = auth_json['access_token']
            refresh_token = auth_json['refresh_token']
            header = {'Authorization': f'Bearer {access_token}'}

            return header, refresh_token
        else:
            # Log an error message with the status code
            if auth.status_code == 401:
                logger.error(f'Token expired, refreshing token...')
            else:
                logger.error(
                    f'Failed to authenticate to the mangadex API: {auth.status_code}')
            raise Exception(f'Authentication failed: {auth.status_code}')

    # Handle any requests exceptions
    except requests.exceptions.RequestException as e:
        logger.error(f'Failed to authenticate to the mangadex API: {e}')
        raise e


def api_token_refresh(payload):
    """Refresh the Mangadex API token and return the header"""
    try:
        refresh = requests.post(AUTH_URL, data=payload)
        if refresh.status_code == 200:
            refresh_json = refresh.json()
            access_token = refresh_json['access_token']
            refresh_token = refresh_json['refresh_token']

            # Update the header with the new access token
            header = {'Authorization': f'Bearer {access_token}'}

            return header, refresh_token
        else:
            logger.error(
                f'Failed to refresh the token for the mangadex API: {refresh.status_code}')
            raise Exception(f'Token Refresh failed: {refresh.status_code}')

    # Handle any requests exceptions
    except requests.exceptions.RequestException as e:
        logger.error(f'Failed to refresh the token for the mangadex API: {e}')
        raise e


def get_latest_manga_feed(header):
    """
    Get the user's followed manga updated list and return a dictionary 
    of chapters
    """
    try:
        response = requests.get(FEED_URL, headers=header, params=FEED_PARAMS)
        if response.status_code == 200:
            manga_feed = response.json()

            if 'data' in manga_feed:
                chapters = {}
                for chapter in manga_feed['data']:
                    chapter_info = {}

                    chapter_id = chapter['id']
                    chapter_number = chapter['attributes']['chapter']
                    language = chapter['attributes']['translatedLanguage']

                    # Get the manga title from the relationships
                    manga_title = None
                    for relation in chapter['relationships']:
                        if relation['type'] == 'manga':
                            manga_title = relation['attributes']['title']

                    # Use the get method to handle missing keys in the dictionary
                    # to get the manga's title
                    if type(manga_title) == dict:
                        manga_title = (
                            manga_title.get('en')
                            or manga_title.get('ja-ro')
                            or manga_title.get('ja')
                            or manga_title.get('es-la')
                        )

                    # Get the chapter's title
                    title = chapter['attributes']['title']
                    if type(title) == dict:
                        title = (
                            title.get('en')
                            or title.get('ja-ro')
                            or title.get('es-la')
                        )

                    # Use default values for missing attributes
                    chapter_info["manga_title"] = manga_title or "Manga title not available"
                    chapter_info["chapter_title"] = title or "Chapter title not available"
                    chapter_info["url"] = f"https://mangadex.org/chapter/{chapter_id}"
                    chapter_info["chapter_number"] = chapter_number
                    chapter_info["language"] = language

                    # Use the chapter_id as the key for the chapters dictionary
                    chapters[chapter_id] = chapter_info

                # Log a success message
                logger.info(
                    "Succesfully retrieved the latest manga feed from the mangadex API")

                return chapters
            else:
                # Log an error message with the status code
                logger.error(
                    f'Data not found: {manga_feed}')
                raise Exception(f'Retrieval failed: {manga_feed}')
        else:
            logger.error(
                f"Failed to retrieve the latest manga feed from the mangadex API: {response.status_code}")
            raise Exception(f"Retrieval failed: {response.status_code}")

    # Handle any requests exceptions
    except requests.exceptions.RequestException as e:
        # Log an error message with the exception
        logger.error(
            f"Failed to retrieve the latest manga feed from the mangadex API: {e}")
        # Raise the exception
        raise e
