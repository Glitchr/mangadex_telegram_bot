import requests
from decouple import config


TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')
url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

def send_chapter(chapter):
    """Sends the new chapter information to the telegram chat"""
    response = requests.post(url, data={
                                'chat_id': TELEGRAM_CHAT_ID,
                                'text': chapter})
