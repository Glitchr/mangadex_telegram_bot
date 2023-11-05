def readable_chapter(chapter_info):
    """Return a readable string of a chapter_info dictionary"""
    return f"{chapter_info['manga_title']} - {chapter_info['chapter_title']} by {chapter_info['author']} ({chapter_info['url']})"
