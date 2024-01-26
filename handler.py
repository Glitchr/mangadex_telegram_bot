"""This module handles sending the chapters to the telegram bot"""

import requests
from decouple import config
from log import logger


TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')
url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'


def send_chapter(chapter):
    """Sends the new chapter information to the telegram chat"""

    try:
        # Send a POST request with the parameters
        response = requests.post(url, data={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': chapter})
        # Check the status code and the response content
        if response.status_code == 200:
            # Log a success message
            logger.info(f"Successfully sent message: {chapter}")
            print("Message sent successfully!")
        else:
            # Log an error message with the status code
            logger.error(
                f"Failed to send message: \n{response.text}\n{chapter}", exc_info=True)
            print("Something went wrong!")
            print(response.text)

    # Handle any requests exceptions
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message: {chapter}", exc_info=True)
        raise e
