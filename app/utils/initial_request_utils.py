import requests
import sys
import yaml
import os
from .uuid_utils import generate_uuid, load_uuid, save_uuid

def load_config(config_file):
    default_config = {"server_url": "http://abc.com", "uuid": ""}

    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f)
        print(f"Configuration file '{config_file}' created with default values.")

    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            # Ensure server_url is present in the config
            if 'server_url' not in config:
                config['server_url'] = default_config['server_url']
            # Load or generate UUID if not present
            if not config.get('uuid'):
                config['uuid'] = load_uuid(config_file) or generate_uuid()
                save_uuid(config['uuid'], config_file)
                with open(config_file, 'w') as f:
                    yaml.dump(config, f)
            return config
    except yaml.YAMLError:
        print(f"Error decoding YAML from '{config_file}'.")
        sys.exit(1)

def register_device(config_file):
    config = load_config(config_file)
    server_url = config.get('server_url')
    device_uuid = config.get('uuid')

    try:
        response = requests.post(f'{server_url}/init-cluster', json={'uuid': device_uuid})
        if response.status_code == 200:
            print("Registration successful")
        else:
            print(f"Registration failed with status code: {response.status_code}")
            sys.exit(1)
    except requests.RequestException as e:
        print(f"Registration failed with exception: {e}")
        sys.exit(1)