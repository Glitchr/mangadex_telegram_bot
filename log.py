import logging


# Create a logger object with the name of the module
logger = logging.getLogger(__name__)
# Set the logging level to INFO
logger.setLevel(logging.INFO)
# Create a file handler object to write the logs to a file
file_handler = logging.FileHandler("mangadex.log", encoding='utf-8')
# Create a formatter object to format the logs
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# Set the formatter for the file handler
file_handler.setFormatter(formatter)
# Add the file handler to the logger, if it is not already added
if not logger.hasHandlers():
    logger.addHandler(file_handler)
