def readable_chapter(chapter_info):
    """Return a readable string of a chapter_info dictionary"""
    return f"{chapter_info['manga_title']}\nChapter {chapter_info['chapter_number']}: {chapter_info['chapter_title']}\nLanguage: {chapter_info['language']}\nby {chapter_info['author']}\n({chapter_info['url']})"
