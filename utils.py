def readable_chapter(chapter_info):
    """Return a readable string of a chapter_info dictionary"""
    if chapter_info['language'] == 'es-la':
        chapter_info['language'] = '\U0001F1F2\U0001F1FD' # Mexican flag
    elif chapter_info['language'] == 'en':
        chapter_info['language'] = '\U0001F1EC\U0001F1E7' # British flag
    return f"{chapter_info['manga_title']}\nChapter {chapter_info['chapter_number']}: {chapter_info['chapter_title']}\nLanguage: {chapter_info['language']}\nTranslated by {chapter_info['scanlation_group']}\n({chapter_info['url']})"
