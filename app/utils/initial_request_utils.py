import logging
import requests
import sys
import os

logger = logging.getLogger('app')

def load_config():
    config = {
        "server_url": os.getenv('SERVER_URL', 'http://localhost:8000'),
        "uuid": os.getenv('UUID', '')
    }
    return config

def register_device():
    config = load_config()
    server_url = config.get('server_url')
    device_uuid = config.get('uuid')

    try:
        response = requests.post(f'{server_url}/api/clusters/init-cluster/', json={'uuid': device_uuid})
        if response.status_code == 200:
            logger.info("Registration request sent ")
        else:
            logger.error(f"Registration request failed with status code: {response.status_code}")
            sys.exit(1)
    except requests.RequestException as e:
        logger.error(f"Registration failed with exception: {e}")
        sys.exit(1)