import uuid
import os
import logging

logger = logging.getLogger(__name__)

def generate_uuid():
    new_uuid = str(uuid.uuid4())
    logger.info(f"Generated new UUID: {new_uuid}")
    return new_uuid

def load_uuid():
    uuid = os.getenv('UUID')
    if uuid:
        logger.info(f"Loaded UUID from environment: {uuid}")
    else:
        logger.warning("UUID not found in environment")
    return uuid

def save_uuid(uuid):
    logger.info(f"UUID cannot be saved to .env file: {uuid}")
    # Note: Environment variables in .env file cannot be modified programmatically.