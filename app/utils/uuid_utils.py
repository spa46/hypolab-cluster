import uuid
import os
import yaml
import logging

logger = logging.getLogger(__name__)

def generate_uuid():
    new_uuid = str(uuid.uuid4())
    logger.info(f"Generated new UUID: {new_uuid}")
    return new_uuid

def load_uuid(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            uuid = config.get('uuid')
            logger.info(f"Loaded UUID from config file: {uuid}")
            return uuid
    return None

def save_uuid(uuid, config_file):
    with open(config_file, 'w') as f:
        yaml.dump({'uuid': uuid}, f)
    logger.info(f"Saved UUID to config file: {uuid}")