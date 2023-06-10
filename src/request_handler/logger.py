import logging
import sys

logger = logging.getLogger(__name__)  # Create a logger instance
logger.setLevel(logging.DEBUG)  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)

# Create a formatter to define the log message format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(funcName)s - %(message)s')

# Create a file handler to write log messages to a file
file_handler = logging.FileHandler('api_client.log')
file_handler.setLevel(logging.DEBUG)  # Set the logging level for the file handler
file_handler.setFormatter(formatter)  # Set the formatter for the file handler

# Create a stream handler to print log messages to the console
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.INFO)  # Set the logging level for the stream handler
stream_handler.setFormatter(formatter)  # Set the formatter for the stream handler

# Add the file handler and stream handler to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)