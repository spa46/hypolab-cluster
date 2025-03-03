import logging
import requests
import sys
import os
import time

from app.utils.uuid_utils import generate_uuid

logger = logging.getLogger('app')

def load_config():
    config = {
        "server_url": os.getenv('SERVER_URL', 'http://localhost:8000'),
        "uuid": os.getenv('UUID', '')
    }
    return config

def save_to_dotenv(key, value):
    with open('.env', 'a') as f:
        f.write(f'\n{key}={value}')

def restart_server():
    for i in range(5, 0, -1):
        logger.info(f"Server restarting in {i} seconds...")
        time.sleep(1)

    os.execv(sys.executable, [sys.executable] + sys.argv)

def register_device():
    config = load_config()
    server_url = config.get('server_url')
    device_uuid = config.get('uuid')

    if not device_uuid:
        device_uuid = generate_uuid()
        logger.info(f"Generated new UUID: {device_uuid}")
        save_to_dotenv('UUID', device_uuid)
        restart_server()

        try:
            response = requests.post(f'{server_url}/api/clusters/init-cluster/', json={'uuid': device_uuid})
            if response.status_code == 200:
                logger.info("Registration request sent")
            else:
                logger.error(f"Registration request failed with status code: {response.status_code}")
                sys.exit(1)
        except requests.RequestException as e:
            logger.error(f"Registration failed with exception: {e}")
            sys.exit(1)