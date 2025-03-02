import logging
import requests
import sys
import yaml
import os
from .uuid_utils import generate_uuid, load_uuid, save_uuid

logger = logging.getLogger('app')

def load_config(config_file):
    default_config = {"server_url": "http://localhost:8000", "uuid": ""}

    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f)
        logger.info(f"Configuration file '{config_file}' created with default values.")

    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            if 'server_url' not in config:
                config['server_url'] = default_config['server_url']
            if not config.get('uuid'):
                config['uuid'] = load_uuid(config_file) or generate_uuid()
                save_uuid(config['uuid'], config_file)
                with open(config_file, 'w') as f:
                    yaml.dump(config, f)
            return config
    except yaml.YAMLError:
        logger.error(f"Error decoding YAML from '{config_file}'.")
        sys.exit(1)

def register_device(config_file):
    config = load_config(config_file)
    server_url = config.get('server_url')
    device_uuid = config.get('uuid')

    try:
        response = requests.post(f'{server_url}/api/hypo/init-cluster/', json={'uuid': device_uuid})
        if response.status_code == 200:
            logger.info("Registration successful")
        else:
            logger.error(f"Registration failed with status code: {response.status_code}")
            sys.exit(1)
    except requests.RequestException as e:
        logger.error(f"Registration failed with exception: {e}")
        sys.exit(1)