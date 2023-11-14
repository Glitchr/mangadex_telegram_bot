import requests


# Define some constants for the mangadex API
BASE_URL = "https://api.mangadex.org"
AUTH_URL = "https://api.mangadex.org/auth/login"
FEED_URL = "https://api.mangadex.org/user/follows/manga/feed"
FEED_PARAMS = {
    "limit": 50,
    "translatedLanguage[]": ["en", "es-la"],
    "order[updatedAt]": "desc",
    "order[volume]": "desc",
    "order[chapter]": "desc",
    "includes[]": ["manga", "cover_art", "author"],
}


def api_auth(payload):
    """Authenticate to the mangadex API and return the header"""
    auth = requests.post(AUTH_URL, json=payload)
    token = auth.json()['token']['session']
    header = {'Authorization': f'Bearer {token}'}

    return header

def get_latest_manga_feed(header):
    """
    Get the user's followed manga updated list and return a dictionary 
    of chapters
    """
    manga_feed = requests.get(FEED_URL, headers=header, params=FEED_PARAMS).json()
    
    chapters = {}
    for chapter in manga_feed["data"]:
        chapter_info = {}

        chapter_id = chapter["id"]
        manga_title = None
        chapter_number = chapter["attributes"]["chapter"]
        language = chapter["attributes"]["translatedLanguage"]
        cover_art = None
        author = None
        url = f"https://mangadex.org/chapter/{chapter_id}"
        for relation in chapter["relationships"]:
            if relation["type"] == "manga":
                manga_title = relation["attributes"]["title"]
            elif relation["type"] == "cover_art":
                cover_art = relation["attributes"]["fileName"]
            elif relation["type"] == "author":
                author = relation["attributes"]["name"]

        # Use the get method to handle missing keys in the dictionary
        if type(manga_title) == dict:
            manga_title = (
                manga_title.get("en")
                or manga_title.get("ja-ro")
                or manga_title.get("es-la")
            )

        # Get the chapter's title
        title = chapter["attributes"]["title"]
        if type(title) == dict:
            title = (
                title.get("en") or title.get("ja-ro") or title.get("es-la")
            )

        # Use default values for missing attributes
        chapter_info["manga_title"] = manga_title or "Manga title not available"
        chapter_info["chapter_title"] = title or "Chapter title not available"
        chapter_info["cover_art"] = cover_art or "Cover art not available"
        chapter_info["author"] = author or "Author not available"
        chapter_info["url"] = url
        chapter_info["chapter_number"] = chapter_number
        chapter_info["language"] = language

        # Use the chapter_id as the key for the chapters dictionary
        chapters[chapter_id] = chapter_info

    return chapters
