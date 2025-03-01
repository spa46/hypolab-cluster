import requests
import sys
import json
from .uuid_utils import generate_uuid, load_uuid, save_uuid

def register_device(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        server_url = config.get('server_url')

    device_uuid = load_uuid(config_file)
    if not device_uuid:
        device_uuid = generate_uuid()
        save_uuid(device_uuid, config_file)

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