import time

def readable_chapter(chapter_info):
    """Return a readable string of a chapter_info dictionary"""
    if chapter_info['language'] == 'es-la':
        chapter_info['language'] = '\U0001F1F2\U0001F1FD' # Mexican flag
    elif chapter_info['language'] == 'en':
        chapter_info['language'] = '\U0001F1EC\U0001F1E7' # British flag
    return f"{chapter_info['manga_title']}\nChapter {chapter_info['chapter_number']}: {chapter_info['chapter_title']}\nLanguage: {chapter_info['language']}\n({chapter_info['url']})"


def retry_on_failure(func, payload, max_retries=5, retry_delay=60):
    """
    Executes a function and implements a retry mechanism if exceptions 
    are raised.
    """
    for attempt in range(max_retries):
        try:
            return func(payload)
        except Exception as e:
            if str(e).startswith('Authentication failed: ') and attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise e
