import logging
import os

logger = logging.getLogger(__name__)

def handle_message(message):
    """Handles incoming Kafka messages."""
    if message == "init-cluster":
        with open('.registration.lock', 'w') as lock_file:
            lock_file.write('')  # Create an empty lock file
        logger.info(".registration.lock file created")